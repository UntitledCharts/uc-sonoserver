import { mkdirSync, writeFileSync } from 'node:fs'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

import ts from 'typescript'

const PACKAGE_NAME = '@sonolus/core'
const LINE_LENGTH = 88
const INDENT = 4

const PYTHON_KEYWORDS = new Set([
    'False',
    'None',
    'True',
    'and',
    'as',
    'assert',
    'async',
    'await',
    'break',
    'class',
    'continue',
    'def',
    'del',
    'elif',
    'else',
    'except',
    'finally',
    'for',
    'from',
    'global',
    'if',
    'import',
    'in',
    'is',
    'lambda',
    'nonlocal',
    'not',
    'or',
    'pass',
    'raise',
    'return',
    'try',
    'while',
    'with',
    'yield',
])

const BASE_MODEL_ATTRIBUTES = new Set([
    'construct',
    'copy',
    'dict',
    'from_orm',
    'json',
    'parse_file',
    'parse_obj',
    'parse_raw',
    'schema',
    'schema_json',
    'update_forward_refs',
    'validate',
])

const RESERVED_NAMES = [
    'Annotated',
    'Any',
    'BaseModel',
    'ConfigDict',
    'Field',
    'Generic',
    'Literal',
    'SonolusModel',
    'TypeAlias',
    'TypeAliasType',
    'TypeVar',
]

const RUNTIME_NAMES = new Set([
    ...RESERVED_NAMES,
    'None',
    'True',
    'False',
    'bool',
    'dict',
    'float',
    'int',
    'list',
    'str',
    'tuple',
    '...',
])

/**
 * Runs the generator using the optional output path given on the command line.
 */
function main() {
    const scriptDirectory = dirname(fileURLToPath(import.meta.url))
    const outputPath = resolve(
        process.argv[2] ?? resolve(scriptDirectory, '../../app/sonolus_core.py'),
    )
    const { entry, version, packageDirectory } = resolvePackage(scriptDirectory)
    const program = ts.createProgram({ rootNames: [entry], options: compilerOptions() })
    const checker = program.getTypeChecker()
    const sourceFile = program.getSourceFile(entry)
    const moduleSymbol = sourceFile && checker.getSymbolAtLocation(sourceFile)
    if (!moduleSymbol) throw new Error(`cannot load the ${PACKAGE_NAME} entry point ${entry}`)

    const state = createState(checker, version)
    collectExports(state, moduleSymbol)
    collectPackageTypes(state, program, packageDirectory)
    convertExports(state)
    pruneBrokenExports(state)
    const { code, summary } = emitModule(state)

    mkdirSync(dirname(outputPath), { recursive: true })
    writeFileSync(outputPath, code)

    const messages = [...state.messages].sort((a, b) => compareText(a.key, b.key))
    for (const message of messages) process.stderr.write(`${message.text}\n`)
    process.stderr.write(
        `wrote ${summary.models} models, ${summary.constants} constant classes and ${summary.aliases} type aliases from ${PACKAGE_NAME} ${version} to ${outputPath}\n`,
    )
}

/**
 * Builds the compiler options used to load the package declarations.
 * @returns {import('typescript').CompilerOptions} Compiler options for the program.
 */
function compilerOptions() {
    return {
        module: ts.ModuleKind.NodeNext,
        moduleResolution: ts.ModuleResolutionKind.NodeNext,
        target: ts.ScriptTarget.ES2022,
        strict: true,
        skipLibCheck: true,
        noEmit: true,
        types: [],
    }
}

/**
 * Resolves the installed package declaration entry point and its version through TypeScript module resolution.
 * @param {string} baseDirectory Directory the package is resolved from.
 * @returns {{ entry: string, version: string, packageDirectory: string }} Entry declaration file, package version and package root.
 */
function resolvePackage(baseDirectory) {
    const { resolvedModule } = ts.resolveModuleName(
        PACKAGE_NAME,
        resolve(baseDirectory, 'index.ts'),
        compilerOptions(),
        ts.sys,
        undefined,
        undefined,
        ts.ModuleKind.ESNext,
    )
    if (!resolvedModule) throw new Error(`cannot resolve ${PACKAGE_NAME}, run npm install first`)
    const { packageId, resolvedFileName } = resolvedModule
    if (!packageId?.version) throw new Error(`cannot read the ${PACKAGE_NAME} version`)
    return {
        entry: resolvedFileName,
        version: packageId.version,
        packageDirectory: resolvedFileName.slice(
            0,
            resolvedFileName.length - packageId.subModuleName.length,
        ),
    }
}

/**
 * Creates the mutable state shared by every conversion step.
 * @param {import('typescript').TypeChecker} checker Type checker of the loaded program.
 * @param {string} version Version of the source package.
 * @returns {object} Fresh generator state.
 */
function createState(checker, version) {
    return {
        checker,
        source: `${PACKAGE_NAME} ${version}`,
        exports: [],
        exportNameBySymbol: new Map(),
        internalNames: new Map(),
        packageTypeSymbols: new Set(),
        symbolByDeclaredType: new Map(),
        inlineSymbols: new Set(),
        anonymous: new Map(),
        usedNames: new Set(RESERVED_NAMES),
        messages: [],
    }
}

/**
 * Records a message for stderr keyed by the export it belongs to.
 * @param {object} state Generator state.
 * @param {string} key Export name used to order the message.
 * @param {string} text Message text.
 */
function report(state, key, text) {
    state.messages.push({ key, text })
}

/**
 * Compares two strings by code unit order.
 * @param {string} a First string.
 * @param {string} b Second string.
 * @returns {number} Negative, zero or positive like a sort comparator.
 */
function compareText(a, b) {
    if (a < b) return -1
    if (a > b) return 1
    return 0
}

/**
 * Compares two strings treating runs of digits as numbers.
 * @param {string} a First string.
 * @param {string} b Second string.
 * @returns {number} Negative, zero or positive like a sort comparator.
 */
function compareNatural(a, b) {
    const left = a.match(/\d+|\D+/g) ?? []
    const right = b.match(/\d+|\D+/g) ?? []
    for (let index = 0; index < Math.min(left.length, right.length); index++) {
        const x = left[index]
        const y = right[index]
        if (x === y) continue
        if (/^\d/.test(x) && /^\d/.test(y)) return Number(x) - Number(y) || compareText(x, y)
        return compareText(x, y)
    }
    return left.length - right.length
}

/**
 * Resolves a symbol through any import or export aliases.
 * @param {object} state Generator state.
 * @param {import('typescript').Symbol} symbol Symbol to resolve.
 * @returns {import('typescript').Symbol} The aliased target or the symbol itself.
 */
function resolveAlias(state, symbol) {
    return symbol.flags & ts.SymbolFlags.Alias ? state.checker.getAliasedSymbol(symbol) : symbol
}

/**
 * Collects every export of the package entry point and classifies it as a type, a constant collection or a skipped value.
 * @param {object} state Generator state.
 * @param {import('typescript').Symbol} moduleSymbol Symbol of the entry module.
 */
function collectExports(state, moduleSymbol) {
    const symbols = state.checker
        .getExportsOfModule(moduleSymbol)
        .sort((a, b) => compareText(a.getName(), b.getName()))

    for (const symbol of symbols) {
        const name = symbol.getName()
        const target = resolveAlias(state, symbol)
        const typeSymbol = [symbol, target].find(
            (candidate) => candidate.flags & (ts.SymbolFlags.TypeAlias | ts.SymbolFlags.Interface),
        )
        const valueSymbol = [target, symbol].find(
            (candidate) => candidate.flags & ts.SymbolFlags.Value,
        )
        const constants = valueSymbol ? readConstants(state, valueSymbol) : null

        if (valueSymbol && !constants) {
            report(state, name, `warning: skipped ${name}: ${describeValue(state, valueSymbol)}`)
        }
        if (constants && typeSymbol) {
            state.inlineSymbols.add(typeSymbol)
            report(
                state,
                name,
                `note: type ${name} is the value union of constant class ${name}, references are inlined as Literal or str`,
            )
        }
        if (!constants && !typeSymbol) continue

        state.usedNames.add(name)
        if (typeSymbol && !constants) state.exportNameBySymbol.set(typeSymbol, name)
        state.exports.push(createRecord(name, constants ? undefined : typeSymbol, constants, null))
    }
}

/**
 * Creates the record that collects everything generated for one named type or constant collection.
 * @param {string} name Python name of the record.
 * @param {import('typescript').Symbol | undefined} typeSymbol Type alias or interface symbol, if any.
 * @param {{ name: string, value: string }[] | null} constants Constants of a constant collection.
 * @param {string | null} internalFor Export that first referenced a non-exported type, or null for exports.
 * @returns {object} Fresh record.
 */
function createRecord(name, typeSymbol, constants, internalFor) {
    return {
        name,
        typeSymbol,
        constants,
        internalFor,
        classes: [],
        alias: null,
        deps: new Set(),
        allocated: [],
        notes: [],
        error: null,
        skipped: false,
    }
}

/**
 * Indexes every type alias and interface declared by the package, reserving names for the non-exported ones.
 * @param {object} state Generator state.
 * @param {import('typescript').Program} program Loaded program.
 * @param {string} packageDirectory Root directory of the installed package.
 */
function collectPackageTypes(state, program, packageDirectory) {
    const internal = []
    for (const sourceFile of program.getSourceFiles()) {
        if (!sourceFile.fileName.startsWith(packageDirectory)) continue
        for (const statement of sourceFile.statements) {
            if (!ts.isTypeAliasDeclaration(statement) && !ts.isInterfaceDeclaration(statement))
                continue
            const symbol = state.checker.getSymbolAtLocation(statement.name)
            if (!symbol || state.packageTypeSymbols.has(symbol)) continue
            state.packageTypeSymbols.add(symbol)
            if (!state.exportNameBySymbol.has(symbol) && !state.inlineSymbols.has(symbol)) {
                internal.push({ symbol, fileName: sourceFile.fileName })
            }
        }
    }

    internal.sort(
        (a, b) =>
            compareText(a.symbol.getName(), b.symbol.getName()) ||
            compareText(a.fileName, b.fileName),
    )
    for (const { symbol } of internal) {
        let name = symbol.getName()
        for (let index = 2; state.usedNames.has(name); index++) name = `${symbol.getName()}${index}`
        state.usedNames.add(name)
        state.internalNames.set(symbol, name)
    }

    const ordered = [...state.exportNameBySymbol.keys(), ...internal.map((entry) => entry.symbol)]
    for (const symbol of ordered) {
        if (typeParameterNames(symbol).length) continue
        const type = state.checker.getDeclaredTypeOfSymbol(symbol)
        if (
            type.aliasSymbol &&
            type.aliasSymbol !== symbol &&
            state.packageTypeSymbols.has(type.aliasSymbol)
        ) {
            continue
        }
        if (!state.symbolByDeclaredType.has(type)) state.symbolByDeclaredType.set(type, symbol)
    }
}

/**
 * Reads an `export * as Name` namespace whose members are all string constants.
 * @param {object} state Generator state.
 * @param {import('typescript').Symbol} symbol Value symbol of the export.
 * @returns {{ name: string, value: string }[] | null} The constants, or null when the value is not a string constant collection.
 */
function readConstants(state, symbol) {
    if (!(symbol.flags & ts.SymbolFlags.ValueModule)) return null
    const members = state.checker.getExportsOfModule(symbol)
    if (!members.length) return null

    const constants = []
    for (const member of members) {
        const resolved = resolveAlias(state, member)
        if (!(resolved.flags & ts.SymbolFlags.Variable)) return null
        const type = state.checker.getTypeOfSymbol(resolved)
        if (!(type.flags & ts.TypeFlags.StringLiteral)) return null
        constants.push({ name: member.getName(), value: type.value })
    }
    return constants
}

/**
 * Describes why a value export cannot be represented.
 * @param {object} state Generator state.
 * @param {import('typescript').Symbol} symbol Value symbol of the export.
 * @returns {string} Human readable reason.
 */
function describeValue(state, symbol) {
    if (symbol.flags & ts.SymbolFlags.ValueModule) {
        return 'namespace export that is not a string constant collection'
    }
    const type = state.checker.getTypeOfSymbol(symbol)
    if (type.getCallSignatures().length) return 'function export'
    return `value export of type ${state.checker.typeToString(type)}`
}

/**
 * Converts every type export, rolling back the ones that cannot be represented.
 * @param {object} state Generator state.
 */
function convertExports(state) {
    for (const record of [...state.exports]) {
        if (record.typeSymbol) convertRecord(state, record)
    }
}

/**
 * Converts the type of one record, rolling it back when it cannot be represented.
 * @param {object} state Generator state.
 * @param {object} record Record to convert.
 */
function convertRecord(state, record) {
    try {
        convertType(state, record)
    } catch (error) {
        record.error = error instanceof Error ? error.message : String(error)
        rollback(state, record)
    }
}

/**
 * Returns the Python name of a named package type, generating a non-exported one on first use.
 * @param {object} state Generator state.
 * @param {import('typescript').Symbol} symbol Type alias or interface symbol.
 * @param {object} context Render context of the referencing type.
 * @returns {string | undefined} Python name, or undefined when the symbol is not a package type.
 */
function packageTypeName(state, symbol, context) {
    const exported = state.exportNameBySymbol.get(symbol)
    if (exported) return exported
    const name = state.internalNames.get(symbol)
    if (!name) return undefined

    state.exportNameBySymbol.set(symbol, name)
    const record = createRecord(
        name,
        symbol,
        null,
        context.record.internalFor ?? context.record.name,
    )
    record.notes.push(
        `note: ${name} is not exported by the entry point, generated because ${record.internalFor} references it`,
    )
    state.exports.push(record)
    convertRecord(state, record)
    return name
}

/**
 * Removes every class and name produced by a failed export.
 * @param {object} state Generator state.
 * @param {object} record Export record to roll back.
 */
function rollback(state, record) {
    for (const [type, model] of state.anonymous) {
        if (model.owner === record) state.anonymous.delete(type)
    }
    for (const name of record.allocated) state.usedNames.delete(name)
    record.classes = []
    record.alias = null
    record.notes = []
}

/**
 * Marks failed exports and every export that depends on them as skipped.
 * @param {object} state Generator state.
 */
function pruneBrokenExports(state) {
    const reasons = new Map()
    for (const record of state.exports) {
        if (record.error) reasons.set(record.name, record.error)
    }
    state.exports.sort((a, b) => compareText(a.name, b.name))

    let changed = true
    while (changed) {
        changed = false
        for (const record of state.exports) {
            if (reasons.has(record.name)) continue
            const missing = [...record.deps].sort(compareText).find((dep) => reasons.has(dep))
            if (missing) {
                reasons.set(record.name, `depends on skipped ${missing}`)
                changed = true
            }
        }
    }

    const byName = new Map(state.exports.map((record) => [record.name, record]))
    const reachable = new Set()
    const queue = state.exports.filter((record) => !record.internalFor && !reasons.has(record.name))
    while (queue.length) {
        const record = queue.pop()
        if (reachable.has(record.name)) continue
        reachable.add(record.name)
        for (const dep of record.deps) if (byName.has(dep)) queue.push(byName.get(dep))
    }

    for (const record of state.exports) {
        if (reasons.has(record.name)) {
            record.skipped = true
            report(
                state,
                record.name,
                `warning: skipped ${record.name}: ${reasons.get(record.name)}`,
            )
        } else if (!reachable.has(record.name)) {
            record.skipped = true
        } else {
            for (const note of record.notes) report(state, record.name, note)
        }
    }
}

/**
 * Reads the declared type parameter names of a type alias or interface.
 * @param {import('typescript').Symbol} symbol Type symbol.
 * @returns {string[]} Type parameter names in declaration order.
 */
function typeParameterNames(symbol) {
    const names = []
    for (const declaration of symbol.declarations ?? []) {
        if (!ts.isTypeAliasDeclaration(declaration) && !ts.isInterfaceDeclaration(declaration)) {
            continue
        }
        for (const parameter of declaration.typeParameters ?? []) {
            if (!names.includes(parameter.name.text)) names.push(parameter.name.text)
        }
    }
    return names
}

/**
 * Converts one exported type alias or interface into a model class or a type alias.
 * @param {object} state Generator state.
 * @param {object} record Export record to fill.
 */
function convertType(state, record) {
    const symbol = record.typeSymbol
    const typeParameters = typeParameterNames(symbol)
    const type = state.checker.getDeclaredTypeOfSymbol(symbol)
    const context = {
        state,
        record,
        self: symbol,
        hint: record.name,
        path: record.name,
        typeParameters,
        typeVars: new Set(),
    }

    if (isModelType(state, type)) {
        record.classes.push(buildExportedModel(context, type))
        return
    }

    record.alias = {
        name: record.name,
        value: renderType(type, context, true),
        typeParameters,
    }
}

/**
 * Checks whether a top-level type should become a model class.
 * @param {object} state Generator state.
 * @param {import('typescript').Type} type Declared type of the export.
 * @returns {boolean} True when the type is an object shape.
 */
function isModelType(state, type) {
    if (type.flags & ts.TypeFlags.NonPrimitive) return true
    if (type.flags & ts.TypeFlags.Intersection) {
        return type.types.every((part) => isObjectShape(state, part))
    }
    if (!isObjectShape(state, type)) return false
    return (
        visibleProperties(state, type).length > 0 ||
        state.checker.getIndexInfosOfType(type).length === 0
    )
}

/**
 * Checks whether a type is a plain object shape rather than an array, tuple or function.
 * @param {object} state Generator state.
 * @param {import('typescript').Type} type Type to inspect.
 * @returns {boolean} True for object shapes.
 */
function isObjectShape(state, type) {
    if (type.flags & ts.TypeFlags.Intersection) {
        return type.types.every((part) => isObjectShape(state, part))
    }
    if (!(type.flags & ts.TypeFlags.Object)) return false
    if (state.checker.isArrayType(type) || state.checker.isTupleType(type)) return false
    return !type.getCallSignatures().length && !type.getConstructSignatures().length
}

/**
 * Lists the string-keyed properties of a type.
 * @param {object} state Generator state.
 * @param {import('typescript').Type} type Type to inspect.
 * @returns {import('typescript').Symbol[]} Properties in checker order.
 */
function visibleProperties(state, type) {
    return state.checker
        .getPropertiesOfType(type)
        .filter((property) => !property.getName().startsWith('__@'))
}

/**
 * Builds the model class of an exported object type.
 * @param {object} context Render context of the export.
 * @param {import('typescript').Type} type Declared type of the export.
 * @returns {object} Class record.
 */
function buildExportedModel(context, type) {
    const { record } = context
    const model = {
        name: record.name,
        doc: record.name,
        bases: [],
        fields: [],
        typeParameters: context.typeParameters,
        owner: record,
    }

    const reference = renderReference(type, context, true)
    if (reference) {
        model.bases = [reference]
    } else {
        const body = buildClassBody(type, context)
        model.bases = body.bases
        model.fields = body.fields
    }
    if (model.typeParameters.length) model.bases.push(genericBase(model.typeParameters))
    return model
}

/**
 * Builds the bases and fields of a model class from an object or intersection type.
 * @param {import('typescript').Type} type Object or intersection type.
 * @param {object} context Render context of the class.
 * @returns {{ bases: object[], fields: object[] }} Class bases and fields.
 */
function buildClassBody(type, context) {
    if (type.flags & ts.TypeFlags.Intersection) {
        const references = type.types.map((part) => renderReference(part, context, false))
        if (references.every(Boolean)) return { bases: references, fields: [] }
    }
    return { bases: [atom('SonolusModel')], fields: renderFields(type, context) }
}

/**
 * Creates the `Generic[...]` base for a list of type parameters.
 * @param {string[]} typeParameters Type parameter names.
 * @returns {object} Python subscript expression.
 */
function genericBase(typeParameters) {
    return subscript(atom('Generic'), typeParameters.map(atom))
}

/**
 * Renders the fields of an object type.
 * @param {import('typescript').Type} type Object type.
 * @param {object} context Render context of the owning class.
 * @returns {object[]} Field records.
 */
function renderFields(type, context) {
    const { state } = context
    const properties = visibleProperties(state, type)
    if (properties.length && state.checker.getIndexInfosOfType(type).length) {
        throw new Error(`${context.path} mixes properties with an index signature`)
    }

    const mapped = Boolean(
        type.flags & ts.TypeFlags.Object && type.objectFlags & ts.ObjectFlags.Mapped,
    )
    if (mapped) properties.sort((a, b) => compareNatural(a.getName(), b.getName()))
    const types = properties.map((property) => propertyType(state, property))
    const shared = mapped && types.length > 1 && types.every((item) => item === types[0])
    const used = new Set()

    return properties.map((property, index) => {
        if (property.flags & ts.SymbolFlags.Method) {
            throw new Error(`${context.path}.${property.getName()} is a method`)
        }
        const key = property.getName()
        const optional = Boolean(property.flags & ts.SymbolFlags.Optional)
        const expression = renderType(types[index], {
            ...context,
            hint: shared ? `${context.hint}Value` : `${context.hint}${pascal(key)}`,
            path: shared
                ? `${context.path}[keyof ${context.path}]`
                : `${context.path}[${JSON.stringify(key)}]`,
        })
        return {
            key,
            name: fieldName(key, used),
            expression: optional ? withNone(expression) : expression,
            optional,
        }
    })
}

/**
 * Reads the type of a property, preferring its written annotation so aliases are preserved.
 * @param {object} state Generator state.
 * @param {import('typescript').Symbol} property Property symbol.
 * @returns {import('typescript').Type} Property type.
 */
function propertyType(state, property) {
    const declaration = property.valueDeclaration
    if (
        !(property.flags & ts.SymbolFlags.Transient) &&
        declaration &&
        (ts.isPropertySignature(declaration) || ts.isPropertyDeclaration(declaration)) &&
        declaration.type
    ) {
        return state.checker.getTypeFromTypeNode(declaration.type)
    }
    return state.checker.getTypeOfSymbol(property)
}

/**
 * Turns a JSON key into a valid pydantic field name.
 * @param {string} key JSON key.
 * @param {Set<string>} used Field names already taken in the class.
 * @returns {string} Python field name.
 */
function fieldName(key, used) {
    let name = key.replace(/[^A-Za-z0-9_]/g, '_').replace(/^_+/, '')
    if (!name || /^[0-9]/.test(name)) name = `field_${name}`
    if (
        name !== key ||
        PYTHON_KEYWORDS.has(name) ||
        BASE_MODEL_ATTRIBUTES.has(name) ||
        name.startsWith('model_')
    ) {
        name = `${name}_`
    }
    while (used.has(name)) name = `${name}_`
    used.add(name)
    return name
}

/**
 * Turns a constant name into a valid Python class attribute name.
 * @param {string} name Constant name.
 * @param {Set<string>} used Attribute names already taken in the class.
 * @returns {string} Python attribute name.
 */
function constantName(name, used) {
    let result = name.replace(/[^A-Za-z0-9_]/g, '_')
    if (/^[0-9]/.test(result)) result = `_${result}`
    if (PYTHON_KEYWORDS.has(result)) result = `${result}_`
    while (used.has(result)) result = `${result}_`
    used.add(result)
    return result
}

/**
 * Renders a TypeScript type as a Python type expression.
 * @param {import('typescript').Type} type Type to render.
 * @param {object} context Render context.
 * @param {boolean} [isTop] True when rendering the declared type of the export itself.
 * @returns {object} Python expression.
 */
function renderType(type, context, isTop = false) {
    return renderReference(type, context, isTop) ?? renderStructure(type, context)
}

/**
 * Renders a reference to another generated export when the type is one.
 * @param {import('typescript').Type} type Type to render.
 * @param {object} context Render context.
 * @param {boolean} isTop True when the export's own name must not be referenced.
 * @returns {object | null} Python expression, or null when the type is not a named export.
 */
function renderReference(type, context, isTop) {
    const { state } = context
    const reference = referencedSymbol(state, type)
    if (!reference || state.inlineSymbols.has(reference.symbol)) return null
    if (isTop && reference.symbol === context.self) return null
    const name = packageTypeName(state, reference.symbol, context)
    return name ? namedReference(name, reference.typeArguments, context) : null
}

/**
 * Finds the named package type alias or interface a type refers to.
 * @param {object} state Generator state.
 * @param {import('typescript').Type} type Type to inspect.
 * @returns {{ symbol: import('typescript').Symbol, typeArguments: readonly import('typescript').Type[] } | null} The referenced symbol and its type arguments.
 */
function referencedSymbol(state, type) {
    if (type.aliasSymbol && state.packageTypeSymbols.has(type.aliasSymbol)) {
        return { symbol: type.aliasSymbol, typeArguments: type.aliasTypeArguments ?? [] }
    }
    if (type.flags & ts.TypeFlags.Object) {
        const isReference = Boolean(type.objectFlags & ts.ObjectFlags.Reference)
        const target = isReference ? type.target : type
        if (target.symbol && state.packageTypeSymbols.has(target.symbol)) {
            return {
                symbol: target.symbol,
                typeArguments: isReference
                    ? state.checker
                          .getTypeArguments(type)
                          .slice(0, target.typeParameters?.length ?? 0)
                    : [],
            }
        }
    }
    const symbol = state.symbolByDeclaredType.get(type)
    return symbol ? { symbol, typeArguments: [] } : null
}

/**
 * Builds a reference to a named export, recording the dependency.
 * @param {string} name Export name.
 * @param {readonly import('typescript').Type[]} typeArguments Type arguments of the reference.
 * @param {object} context Render context.
 * @returns {object} Python expression.
 */
function namedReference(name, typeArguments, context) {
    if (name !== context.record.name) context.record.deps.add(name)
    if (!typeArguments.length) return atom(name)
    return subscript(
        atom(name),
        typeArguments.map((argument, index) =>
            renderType(argument, {
                ...context,
                hint: `${context.hint}Argument${index + 1}`,
                path: `${context.path} argument ${index + 1}`,
            }),
        ),
    )
}

/**
 * Renders a type by its structure.
 * @param {import('typescript').Type} type Type to render.
 * @param {object} context Render context.
 * @returns {object} Python expression.
 */
function renderStructure(type, context) {
    const flags = type.flags
    if (flags & (ts.TypeFlags.Any | ts.TypeFlags.Unknown)) return atom('Any')
    if (flags & ts.TypeFlags.TypeParameter) return renderTypeParameter(type, context)
    if (flags & ts.TypeFlags.Boolean) return atom('bool')
    if (flags & ts.TypeFlags.Union) return renderUnion(type.types, context)
    if (flags & ts.TypeFlags.Intersection) return renderIntersection(type, context)
    if (flags & (ts.TypeFlags.String | ts.TypeFlags.TemplateLiteral | ts.TypeFlags.StringMapping)) {
        return atom('str')
    }
    if (flags & ts.TypeFlags.Number) return numberExpression()
    if (
        flags &
        (ts.TypeFlags.StringLiteral | ts.TypeFlags.NumberLiteral | ts.TypeFlags.BooleanLiteral)
    ) {
        return literalExpression([literalValue(context.state, type)])
    }
    if (flags & (ts.TypeFlags.Null | ts.TypeFlags.Undefined)) return atom('None')
    if (flags & ts.TypeFlags.NonPrimitive)
        return subscript(atom('dict'), [atom('str'), atom('Any')])
    if (flags & ts.TypeFlags.Object) return renderObject(type, context)
    throw new Error(
        `unsupported type ${context.state.checker.typeToString(type)} at ${context.path}`,
    )
}

/**
 * Renders a type parameter as its module level TypeVar.
 * @param {import('typescript').Type} type Type parameter.
 * @param {object} context Render context.
 * @returns {object} Python expression.
 */
function renderTypeParameter(type, context) {
    const name = type.symbol?.getName()
    if (!name || !context.typeParameters.includes(name)) {
        throw new Error(`unbound type parameter ${name ?? '?'} at ${context.path}`)
    }
    context.typeVars.add(name)
    return atom(name)
}

/**
 * Reads the JavaScript value of a literal type.
 * @param {object} state Generator state.
 * @param {import('typescript').Type} type String, number or boolean literal type.
 * @returns {string | number | boolean} Literal value.
 */
function literalValue(state, type) {
    if (type.flags & ts.TypeFlags.BooleanLiteral) return state.checker.typeToString(type) === 'true'
    return type.value
}

/**
 * Renders a union, collapsing literals, primitives and discriminated object members.
 * @param {readonly import('typescript').Type[]} types Union members.
 * @param {object} context Render context.
 * @returns {object} Python expression.
 */
function renderUnion(types, context) {
    const { state } = context
    const literals = []
    const members = []
    let nullable = false

    for (const member of types) {
        if (member.flags & (ts.TypeFlags.Null | ts.TypeFlags.Undefined)) nullable = true
        else if (
            member.flags &
            (ts.TypeFlags.StringLiteral | ts.TypeFlags.NumberLiteral | ts.TypeFlags.BooleanLiteral)
        ) {
            literals.push(literalValue(state, member))
        } else members.push(member)
    }

    const variants = variantNames(
        state,
        members.filter((member) => isAnonymousObject(state, member)),
        context.hint,
    )
    const objects = []
    const others = []
    for (const member of members) {
        const variant = variants.get(member)
        const expression = renderType(
            member,
            variant ? { ...context, hint: variant, path: `${context.path} variant` } : context,
        )
        if (isObjectShape(state, member) && isModelExpression(expression)) {
            objects.push({ type: member, expression })
        } else others.push(expression)
    }

    const flattened = others.flatMap((expression) =>
        expression.kind === 'union' ? expression.items : [expression],
    )
    const stringish = hasAtom(flattened, 'str')
    const numeric = hasAtom(flattened, 'int') || hasAtom(flattened, 'float')
    const boolean =
        hasAtom(flattened, 'bool') || (literals.includes(true) && literals.includes(false))
    for (const item of flattened) {
        if (item.kind === 'subscript' && flat(item.base) === 'Literal') {
            literals.push(...item.literalValues)
        }
        if (item.kind === 'atom' && item.text === 'None') nullable = true
    }

    const parts = []
    if (stringish) parts.push(atom('str'))
    if (numeric) parts.push(atom('int'), atom('float'))
    if (boolean) parts.push(atom('bool'))
    const remaining = literals.filter(
        (value) =>
            !(typeof value === 'string' && stringish) &&
            !(typeof value === 'number' && numeric) &&
            !(typeof value === 'boolean' && boolean),
    )
    if (remaining.length) parts.push(literalExpression(remaining))
    parts.push(
        ...sortExpressions(
            flattened.filter(
                (item) =>
                    !(
                        item.kind === 'atom' &&
                        ['str', 'int', 'float', 'bool', 'None'].includes(item.text)
                    ) && !(item.kind === 'subscript' && flat(item.base) === 'Literal'),
            ),
        ),
    )

    if (objects.length) {
        const sorted = sortExpressions(objects.map((item) => item.expression))
        const discriminated =
            objects.length > 1 &&
            hasUniqueDiscriminator(
                state,
                objects.map((item) => item.type),
            )
        if (
            objects.length > 1 &&
            !discriminated &&
            objects.every((item) => discriminatorValues(state, item.type))
        ) {
            context.record.notes.push(
                `note: ${context.path} shares "type" values between members, emitted as a plain union`,
            )
        }
        parts.push(
            discriminated
                ? subscript(atom('Annotated'), [
                      unionExpression(sorted),
                      callExpression(atom('Field'), [keyword('discriminator', atom('"type"'))]),
                  ])
                : unionExpression(sorted),
        )
    }
    if (nullable) parts.push(atom('None'))
    if (!parts.length) throw new Error(`empty union at ${context.path}`)
    return unionExpression(parts)
}

/**
 * Checks whether a list of expressions contains a given atom.
 * @param {object[]} items Python expressions.
 * @param {string} text Atom text to look for.
 * @returns {boolean} True when the atom is present.
 */
function hasAtom(items, text) {
    return items.some((item) => item.kind === 'atom' && item.text === text)
}

/**
 * Checks whether an expression refers to a generated model class.
 * @param {object} expression Python expression.
 * @returns {boolean} True for class references, plain or parametrized.
 */
function isModelExpression(expression) {
    const head = expression.kind === 'subscript' ? expression.base : expression
    return head.kind === 'atom' && !RUNTIME_NAMES.has(head.text)
}

/**
 * Reads the literal values of the `type` property of an object member.
 * @param {object} state Generator state.
 * @param {import('typescript').Type} type Object type.
 * @returns {string[] | null} The string literal values, or null when `type` is not a required string literal.
 */
function discriminatorValues(state, type) {
    const property = state.checker.getPropertyOfType(type, 'type')
    if (!property || property.flags & ts.SymbolFlags.Optional) return null
    const propertyType = state.checker.getTypeOfSymbol(property)
    const members = propertyType.flags & ts.TypeFlags.Union ? propertyType.types : [propertyType]
    if (!members.every((member) => member.flags & ts.TypeFlags.StringLiteral)) return null
    return members.map((member) => member.value)
}

/**
 * Checks whether every object member has a literal `type` property with values unique across members.
 * @param {object} state Generator state.
 * @param {import('typescript').Type[]} types Object members of a union.
 * @returns {boolean} True when pydantic can discriminate on `type`.
 */
function hasUniqueDiscriminator(state, types) {
    const seen = new Set()
    for (const type of types) {
        const values = discriminatorValues(state, type)
        if (!values) return false
        for (const value of values) {
            if (seen.has(value)) return false
            seen.add(value)
        }
    }
    return true
}

/**
 * Checks whether a union member is an unnamed object shape that needs a generated class.
 * @param {object} state Generator state.
 * @param {import('typescript').Type} type Union member.
 * @returns {boolean} True for anonymous object shapes with properties.
 */
function isAnonymousObject(state, type) {
    if (!isObjectShape(state, type) || referencedSymbol(state, type)) return false
    return visibleProperties(state, type).length > 0
}

/**
 * Names the anonymous object members of a union from a shared literal property, unique keys or position.
 * @param {object} state Generator state.
 * @param {import('typescript').Type[]} types Anonymous object members.
 * @param {string} base Name hint of the union.
 * @returns {Map<import('typescript').Type, string>} Name hint per member.
 */
function variantNames(state, types, base) {
    const names = new Map()
    if (types.length < 2) return names

    const keySets = types.map((type) =>
        visibleProperties(state, type).map((property) => property.getName()),
    )
    for (const key of keySets[0]) {
        if (!keySets.every((keys) => keys.includes(key))) continue
        const values = types.map((type) => {
            const property = state.checker.getPropertyOfType(type, key)
            const propertyType = property && state.checker.getTypeOfSymbol(property)
            return propertyType &&
                propertyType.flags &
                    (ts.TypeFlags.StringLiteral |
                        ts.TypeFlags.NumberLiteral |
                        ts.TypeFlags.BooleanLiteral)
                ? literalValue(state, propertyType)
                : undefined
        })
        if (values.some((value) => value === undefined) || new Set(values).size !== values.length)
            continue
        types.forEach((type, index) => {
            const value = values[index]
            names.set(
                type,
                typeof value === 'string'
                    ? `${base}${pascal(value)}`
                    : `${base}${pascal(key)}${pascal(String(value))}`,
            )
        })
        if (new Set(names.values()).size === types.length) return names
        names.clear()
    }

    const uniqueKeys = keySets.map((keys, index) =>
        keys.filter((key) =>
            keySets.every((other, otherIndex) => otherIndex === index || !other.includes(key)),
        ),
    )
    const keyNames = uniqueKeys.map((keys) => `${base}${keys.map(pascal).join('')}`)
    if (uniqueKeys.every((keys) => keys.length) && new Set(keyNames).size === types.length) {
        types.forEach((type, index) => names.set(type, keyNames[index]))
        return names
    }

    types.forEach((type, index) => names.set(type, `${base}${index + 1}`))
    return names
}

/**
 * Renders an intersection as a branded primitive or a merged model.
 * @param {import('typescript').Type} type Intersection type.
 * @param {object} context Render context.
 * @returns {object} Python expression.
 */
function renderIntersection(type, context) {
    const { state } = context
    const primitiveFlags =
        ts.TypeFlags.String |
        ts.TypeFlags.Number |
        ts.TypeFlags.Boolean |
        ts.TypeFlags.StringLiteral |
        ts.TypeFlags.NumberLiteral |
        ts.TypeFlags.BooleanLiteral |
        ts.TypeFlags.TemplateLiteral
    const primitives = type.types.filter((part) => part.flags & primitiveFlags)
    const rest = type.types.filter((part) => !(part.flags & primitiveFlags))

    if (primitives.length === 1 && rest.every((part) => isObjectShape(state, part))) {
        return renderStructure(primitives[0], context)
    }
    if (!primitives.length && rest.every((part) => isObjectShape(state, part))) {
        return anonymousModel(type, context)
    }
    throw new Error(
        `unsupported intersection ${state.checker.typeToString(type)} at ${context.path}`,
    )
}

/**
 * Renders an object type as a list, tuple, dict or generated model.
 * @param {import('typescript').Type} type Object type.
 * @param {object} context Render context.
 * @returns {object} Python expression.
 */
function renderObject(type, context) {
    const { state } = context
    const { checker } = state

    if (checker.isArrayType(type)) {
        const [element] = checker.getTypeArguments(type)
        return subscript(atom('list'), [
            renderType(element, {
                ...context,
                hint: singular(context.hint),
                path: `${context.path}[number]`,
            }),
        ])
    }

    if (checker.isTupleType(type)) {
        const elements = checker.getTypeArguments(type)
        const elementFlags = type.target.elementFlags
        if (elementFlags.every((flag) => flag & ts.ElementFlags.Required)) {
            return subscript(
                atom('tuple'),
                elements.map((element, index) => renderTupleElement(element, index, context)),
            )
        }
        if (elements.length === 1 && elementFlags[0] & ts.ElementFlags.Rest) {
            return subscript(atom('tuple'), [
                renderTupleElement(elements[0], 0, context),
                atom('...'),
            ])
        }
        throw new Error(`unsupported tuple ${checker.typeToString(type)} at ${context.path}`)
    }

    if (type.getCallSignatures().length || type.getConstructSignatures().length) {
        throw new Error(`function type ${checker.typeToString(type)} at ${context.path}`)
    }

    const properties = visibleProperties(state, type)
    const indexInfos = checker.getIndexInfosOfType(type)
    if (!properties.length) {
        if (!indexInfos.length) return subscript(atom('dict'), [atom('str'), atom('Any')])
        const [info] = indexInfos
        if (
            indexInfos.length === 1 &&
            info.keyType.flags & (ts.TypeFlags.String | ts.TypeFlags.Number)
        ) {
            return subscript(atom('dict'), [
                atom('str'),
                renderType(info.type, {
                    ...context,
                    hint: `${context.hint}Value`,
                    path: `${context.path}[string]`,
                }),
            ])
        }
        throw new Error(
            `unsupported index signature ${checker.typeToString(type)} at ${context.path}`,
        )
    }
    return anonymousModel(type, context)
}

/**
 * Renders one tuple element type.
 * @param {import('typescript').Type} element Element type.
 * @param {number} index Element position.
 * @param {object} context Render context of the tuple.
 * @returns {object} Python expression.
 */
function renderTupleElement(element, index, context) {
    return renderType(element, {
        ...context,
        hint: `${context.hint}${index + 1}`,
        path: `${context.path}[${index}]`,
    })
}

/**
 * Generates, or reuses, the class of an anonymous object shape and returns a reference to it.
 * @param {import('typescript').Type} type Anonymous object or intersection type.
 * @param {object} context Render context.
 * @returns {object} Python expression referencing the class.
 */
function anonymousModel(type, context) {
    const { state, record } = context
    const existing = state.anonymous.get(type)
    if (existing) {
        if (existing.owner !== record) record.deps.add(existing.owner.name)
        for (const name of existing.typeParameters) context.typeVars.add(name)
        return classReference(existing)
    }

    const name = allocateName(state, context.hint, record)
    const model = {
        name,
        doc: context.path,
        bases: [],
        fields: [],
        typeParameters: [],
        owner: record,
    }
    state.anonymous.set(type, model)
    record.classes.push(model)

    const inner = { ...context, hint: name, typeVars: new Set() }
    const body = buildClassBody(type, inner)
    model.bases = body.bases
    model.fields = body.fields
    model.typeParameters = context.typeParameters.filter((parameter) =>
        inner.typeVars.has(parameter),
    )
    if (model.typeParameters.length) model.bases.push(genericBase(model.typeParameters))
    for (const parameter of model.typeParameters) context.typeVars.add(parameter)
    return classReference(model)
}

/**
 * Builds a reference to a generated class, parametrized by its type parameters.
 * @param {object} model Class record.
 * @returns {object} Python expression.
 */
function classReference(model) {
    if (!model.typeParameters.length) return atom(model.name)
    return subscript(atom(model.name), model.typeParameters.map(atom))
}

/**
 * Reserves a unique module level name for a generated class.
 * @param {object} state Generator state.
 * @param {string} hint Preferred name.
 * @param {object} record Export record that owns the class.
 * @returns {string} Reserved name.
 */
function allocateName(state, hint, record) {
    let name = hint
    for (let index = 2; state.usedNames.has(name); index++) name = `${hint}${index}`
    if (name !== hint) {
        record.notes.push(`note: ${hint} is already taken, generated ${name} for ${record.name}`)
    }
    state.usedNames.add(name)
    record.allocated.push(name)
    return name
}

/**
 * Converts a string into PascalCase.
 * @param {string} text Source text.
 * @returns {string} PascalCase text.
 */
function pascal(text) {
    return text
        .split(/[^A-Za-z0-9]+/)
        .filter(Boolean)
        .map((part) => part[0].toUpperCase() + part.slice(1))
        .join('')
}

/**
 * Derives a singular class name hint for array elements.
 * @param {string} hint Plural name hint.
 * @returns {string} Singular name hint.
 */
function singular(hint) {
    if (/ies$/.test(hint)) return `${hint.slice(0, -3)}y`
    if (/(ch|sh|x|ss)es$/.test(hint)) return hint.slice(0, -2)
    if (/[^su]s$/.test(hint)) return hint.slice(0, -1)
    return hint
}

/**
 * Creates a Python atom such as a name, number or string literal.
 * @param {string} text Source text.
 * @returns {object} Python expression.
 */
function atom(text) {
    return { kind: 'atom', text }
}

/**
 * Creates a Python subscript expression.
 * @param {object} base Subscripted expression.
 * @param {object[]} items Subscript items.
 * @returns {object} Python expression.
 */
function subscript(base, items) {
    return { kind: 'subscript', base, items }
}

/**
 * Creates a Python call expression.
 * @param {object} callee Called expression.
 * @param {object[]} items Positional and keyword arguments.
 * @returns {object} Python expression.
 */
function callExpression(callee, items) {
    return { kind: 'call', callee, items }
}

/**
 * Creates a Python keyword argument.
 * @param {string} key Argument name.
 * @param {object} value Argument value.
 * @returns {object} Python expression.
 */
function keyword(key, value) {
    return { kind: 'keyword', key, value }
}

/**
 * Creates a Python tuple display.
 * @param {object[]} items Tuple items.
 * @returns {object} Python expression.
 */
function tupleExpression(items) {
    return { kind: 'tuple', items }
}

/**
 * Creates a flattened, deduplicated Python `|` union.
 * @param {object[]} items Union members.
 * @returns {object} Python expression, or the only member.
 */
function unionExpression(items) {
    const seen = new Set()
    const flattened = []
    for (const item of items.flatMap((entry) => (entry.kind === 'union' ? entry.items : [entry]))) {
        const text = flat(item)
        if (seen.has(text)) continue
        seen.add(text)
        flattened.push(item)
    }
    return flattened.length === 1 ? flattened[0] : { kind: 'union', items: flattened }
}

/**
 * Creates the `int | float` expression used for TypeScript numbers.
 * @returns {object} Python expression.
 */
function numberExpression() {
    return unionExpression([atom('int'), atom('float')])
}

/**
 * Adds `None` to an expression unless it is already nullable.
 * @param {object} expression Python expression.
 * @returns {object} Nullable Python expression.
 */
function withNone(expression) {
    return unionExpression([expression, atom('None')])
}

/**
 * Creates a sorted `Literal[...]` expression.
 * @param {(string | number | boolean)[]} values Literal values.
 * @returns {object} Python expression carrying its values.
 */
function literalExpression(values) {
    const sorted = [...new Set(values)].sort((a, b) =>
        literalRank(a) !== literalRank(b)
            ? literalRank(a) - literalRank(b)
            : typeof a === 'number'
              ? a - b
              : compareText(String(a), String(b)),
    )
    return {
        ...subscript(
            atom('Literal'),
            sorted.map((value) => atom(pythonLiteral(value))),
        ),
        literalValues: sorted,
    }
}

/**
 * Orders literal kinds as booleans, then numbers, then strings.
 * @param {string | number | boolean} value Literal value.
 * @returns {number} Sort rank of the value kind.
 */
function literalRank(value) {
    if (typeof value === 'boolean') return 0
    if (typeof value === 'number') return 1
    return 2
}

/**
 * Renders a JavaScript literal value as Python source.
 * @param {string | number | boolean} value Literal value.
 * @returns {string} Python source text.
 */
function pythonLiteral(value) {
    if (typeof value === 'boolean') return value ? 'True' : 'False'
    if (typeof value === 'number') return String(value)
    return pythonString(value)
}

/**
 * Quotes a string the way ruff format prefers.
 * @param {string} value String value.
 * @returns {string} Python string literal.
 */
function pythonString(value) {
    const quoted = JSON.stringify(value)
    if (value.includes('"') && !value.includes("'")) {
        return `'${quoted.slice(1, -1).replaceAll('\\"', '"')}'`
    }
    return quoted
}

/**
 * Sorts expressions by their flat source text.
 * @param {object[]} expressions Python expressions.
 * @returns {object[]} Sorted copy.
 */
function sortExpressions(expressions) {
    return [...expressions].sort((a, b) => compareText(flat(a), flat(b)))
}

/**
 * Prints an expression on a single line.
 * @param {object} expression Python expression.
 * @returns {string} Source text.
 */
function flat(expression) {
    switch (expression.kind) {
        case 'atom':
            return expression.text
        case 'subscript':
            return `${flat(expression.base)}[${expression.items.map(flat).join(', ')}]`
        case 'call':
            return `${flat(expression.callee)}(${expression.items.map(flat).join(', ')})`
        case 'keyword':
            return `${expression.key}=${flat(expression.value)}`
        case 'tuple':
            return expression.items.length === 1
                ? `(${flat(expression.items[0])},)`
                : `(${expression.items.map(flat).join(', ')})`
        case 'union':
            return expression.items.map(flat).join(' | ')
        default:
            throw new Error(`unknown expression kind ${expression.kind}`)
    }
}

/**
 * Creates an indentation string.
 * @param {number} width Number of spaces.
 * @returns {string} Spaces.
 */
function spaces(width) {
    return ' '.repeat(width)
}

/**
 * Checks whether a line fits the ruff line length.
 * @param {string} line Source line.
 * @returns {boolean} True when the line fits.
 */
function fits(line) {
    return line.length <= LINE_LENGTH
}

/**
 * Checks whether an expression has its own brackets that ruff can split.
 * @param {object} expression Python expression.
 * @returns {boolean} True for subscripts and calls.
 */
function isBracketed(expression) {
    return expression.kind === 'subscript' || expression.kind === 'call'
}

/**
 * Lays out an expression inside brackets, where unions split without extra parentheses.
 * @param {object} expression Python expression.
 * @param {number} indent Indentation of continuation lines.
 * @param {string} prefix Text before the expression on its first line.
 * @param {string} suffix Text after the expression on its last line.
 * @returns {string[]} Source lines.
 */
function layoutNested(expression, indent, prefix, suffix) {
    const line = `${prefix}${flat(expression)}${suffix}`
    if (fits(line)) return [line]
    if (isBracketed(expression)) return layoutHugged(expression, indent, prefix, suffix)
    if (expression.kind === 'union') {
        return expression.items.flatMap((item, index) =>
            layoutNested(
                item,
                indent,
                index === 0 ? prefix : `${spaces(indent)}| `,
                index === expression.items.length - 1 ? suffix : '',
            ),
        )
    }
    if (expression.kind === 'keyword') {
        return layoutNested(expression.value, indent, `${prefix}${expression.key}=`, suffix)
    }
    return [line]
}

/**
 * Splits a subscript or call at its own brackets.
 * @param {object} expression Subscript or call expression.
 * @param {number} indent Indentation of the line holding the brackets.
 * @param {string} prefix Text before the expression on its first line.
 * @param {string} suffix Text after the closing bracket.
 * @returns {string[]} Source lines.
 */
function layoutHugged(expression, indent, prefix, suffix) {
    const isSubscript = expression.kind === 'subscript'
    const head = flat(isSubscript ? expression.base : expression.callee)
    const inner = indent + INDENT
    const first = `${prefix}${head}${isSubscript ? '[' : '('}`
    const last = `${spaces(indent)}${isSubscript ? ']' : ')'}${suffix}`
    const joined = `${spaces(inner)}${expression.items.map(flat).join(', ')}`
    if (fits(joined)) return [first, joined, last]
    const trailing = isSubscript && expression.items.length === 1 ? '' : ','
    return [
        first,
        ...expression.items.flatMap((item) => layoutNested(item, inner, spaces(inner), trailing)),
        last,
    ]
}

/**
 * Lays out an expression that starts a statement part, parenthesizing unions that must split.
 * @param {object} expression Python expression.
 * @param {number} indent Indentation of the statement.
 * @param {string} prefix Text before the expression.
 * @param {string} suffix Text after the expression.
 * @returns {string[]} Source lines.
 */
function layoutStatementPart(expression, indent, prefix, suffix) {
    const line = `${prefix}${flat(expression)}${suffix}`
    if (fits(line)) return [line]
    if (isBracketed(expression)) return layoutHugged(expression, indent, prefix, suffix)
    if (expression.kind === 'union') {
        return [
            `${prefix}(`,
            ...layoutNested(expression, indent + INDENT, spaces(indent + INDENT), ''),
            `${spaces(indent)})${suffix}`,
        ]
    }
    return [line]
}

/**
 * Lays out an assignment, optionally annotated, following ruff's right-hand-side preference.
 * @param {number} indent Indentation of the statement.
 * @param {string} target Assigned name.
 * @param {object | null} annotation Annotation expression.
 * @param {object} value Assigned value.
 * @returns {string[]} Source lines.
 */
function layoutAssignment(indent, target, annotation, value) {
    const pad = spaces(indent)
    const left = annotation ? `${pad}${target}: ${flat(annotation)}` : `${pad}${target}`
    const single = `${left} = ${flat(value)}`
    if (fits(single)) return [single]

    if (isBracketed(value)) {
        const head = flat(value.kind === 'subscript' ? value.base : value.callee)
        if (fits(`${left} = ${head}${value.kind === 'subscript' ? '[' : '('}`)) {
            return layoutHugged(value, indent, `${left} = `, '')
        }
    }

    const inner = spaces(indent + INDENT)
    if (fits(`${left} = (`) && (value.kind === 'union' || fits(`${inner}${flat(value)}`))) {
        return [`${left} = (`, ...layoutNested(value, indent + INDENT, inner, ''), `${pad})`]
    }

    if (annotation) {
        return layoutStatementPart(annotation, indent, `${pad}${target}: `, ` = ${flat(value)}`)
    }
    return [single]
}

/**
 * Lays out a class header with its bases.
 * @param {string} name Class name.
 * @param {object[]} bases Base class expressions.
 * @returns {string[]} Source lines.
 */
function layoutClassHeader(name, bases) {
    if (!bases.length) return [`class ${name}:`]
    return layoutNested(callExpression(atom(name), bases), 0, 'class ', ':')
}

/**
 * Collects every atom used by an expression.
 * @param {object} expression Python expression.
 * @param {Set<string>} names Set receiving the atom texts.
 */
function collectAtoms(expression, names) {
    switch (expression.kind) {
        case 'atom':
            names.add(expression.text)
            break
        case 'subscript':
            collectAtoms(expression.base, names)
            for (const item of expression.items) collectAtoms(item, names)
            break
        case 'call':
            collectAtoms(expression.callee, names)
            for (const item of expression.items) collectAtoms(item, names)
            break
        case 'keyword':
            collectAtoms(expression.value, names)
            break
        case 'tuple':
        case 'union':
            for (const item of expression.items) collectAtoms(item, names)
            break
        default:
            throw new Error(`unknown expression kind ${expression.kind}`)
    }
}

/**
 * Returns the atoms used by a list of expressions.
 * @param {object[]} expressions Python expressions.
 * @returns {Set<string>} Atom texts.
 */
function atomsOf(expressions) {
    const names = new Set()
    for (const expression of expressions) collectAtoms(expression, names)
    return names
}

/**
 * Orders items alphabetically while placing each item after the items it depends on.
 * @param {object[]} items Items with a `name` property.
 * @param {(item: object) => Set<string>} dependencies Returns the names an item depends on.
 * @returns {object[]} Ordered items.
 */
function topologicalSort(items, dependencies) {
    const byName = new Map(items.map((item) => [item.name, item]))
    const pending = new Map(
        items.map((item) => [
            item.name,
            new Set(
                [...dependencies(item)].filter((name) => byName.has(name) && name !== item.name),
            ),
        ]),
    )
    const ordered = []
    while (pending.size) {
        const ready = [...pending.keys()]
            .filter((name) => !pending.get(name).size)
            .sort(compareText)
        if (!ready.length)
            throw new Error(`cyclic runtime dependency between ${[...pending.keys()].join(', ')}`)
        const [name] = ready
        ordered.push(byName.get(name))
        pending.delete(name)
        for (const set of pending.values()) set.delete(name)
    }
    return ordered
}

/**
 * Orders aliases so that every alias that parametrizes a generic model comes after all aliases its schema needs.
 * @param {object[]} aliases Alias records.
 * @param {object[]} models Class records.
 * @returns {object[]} Ordered aliases.
 */
function orderAliases(aliases, models) {
    const modelNames = new Set(models.map((model) => model.name))
    const aliasNames = new Set(aliases.map((alias) => alias.name))
    const typeVarNames = new Set([
        ...models.flatMap((model) => model.typeParameters),
        ...aliases.flatMap((alias) => alias.typeParameters),
    ])
    const graph = new Map([
        ...models.map((model) => [
            model.name,
            atomsOf([...model.bases, ...model.fields.map((field) => field.expression)]),
        ]),
        ...aliases.map((alias) => [alias.name, atomsOf([alias.value])]),
    ])
    const deepDependencies = new Map(
        aliases.map((alias) => [
            alias.name,
            parametrizesModel(alias.value, modelNames, typeVarNames)
                ? reachableNames(alias.name, graph, aliasNames)
                : atomsOf([alias.value]),
        ]),
    )
    try {
        return topologicalSort(aliases, (alias) => deepDependencies.get(alias.name))
    } catch {
        return topologicalSort(aliases, (alias) => atomsOf([alias.value]))
    }
}

/**
 * Collects the names of a kind reachable from a node of a name graph.
 * @param {string} start Name to start from.
 * @param {Map<string, Set<string>>} graph Names referenced by each class or alias.
 * @param {Set<string>} wanted Names to collect.
 * @returns {Set<string>} Reachable wanted names other than the start.
 */
function reachableNames(start, graph, wanted) {
    const seen = new Set([start])
    const queue = [start]
    const found = new Set()
    while (queue.length) {
        for (const name of graph.get(queue.pop()) ?? []) {
            if (seen.has(name)) continue
            seen.add(name)
            queue.push(name)
            if (wanted.has(name)) found.add(name)
        }
    }
    return found
}

/**
 * Checks whether an expression parametrizes a generated generic model with concrete arguments.
 * @param {object} expression Python expression.
 * @param {Set<string>} modelNames Names of generated classes.
 * @param {Set<string>} typeVarNames Names of module level TypeVars.
 * @returns {boolean} True when the expression creates a parametrized model class at import time.
 */
function parametrizesModel(expression, modelNames, typeVarNames) {
    switch (expression.kind) {
        case 'subscript':
            if (
                expression.base.kind === 'atom' &&
                modelNames.has(expression.base.text) &&
                !expression.items.every(
                    (item) => item.kind === 'atom' && typeVarNames.has(item.text),
                )
            ) {
                return true
            }
            return expression.items.some((item) =>
                parametrizesModel(item, modelNames, typeVarNames),
            )
        case 'call':
        case 'tuple':
        case 'union':
            return expression.items.some((item) =>
                parametrizesModel(item, modelNames, typeVarNames),
            )
        case 'keyword':
            return parametrizesModel(expression.value, modelNames, typeVarNames)
        default:
            return false
    }
}

/**
 * Builds the value expression of a field default.
 * @param {object} field Field record.
 * @returns {object | null} Python expression, or null when the field has no default.
 */
function fieldValue(field) {
    const alias = keyword('alias', atom(pythonString(field.key)))
    if (field.name !== field.key) {
        return callExpression(
            atom('Field'),
            field.optional ? [keyword('default', atom('None')), alias] : [alias],
        )
    }
    return field.optional ? atom('None') : null
}

/**
 * Emits the source lines of a model class.
 * @param {object} model Class record.
 * @param {string} source Package name and version.
 * @returns {string[]} Source lines.
 */
function emitModel(model, source) {
    const lines = [
        ...layoutClassHeader(model.name, model.bases),
        `    """${model.doc} from ${source}."""`,
    ]
    if (model.fields.length) lines.push('')
    for (const field of model.fields) {
        const value = fieldValue(field)
        lines.push(
            ...(value
                ? layoutAssignment(INDENT, field.name, field.expression, value)
                : layoutStatementPart(field.expression, INDENT, `    ${field.name}: `, '')),
        )
    }
    return lines
}

/**
 * Emits the source lines of a constant collection class.
 * @param {object} record Export record with constants.
 * @param {string} source Package name and version.
 * @returns {string[]} Source lines.
 */
function emitConstants(record, source) {
    const used = new Set()
    const lines = [`class ${record.name}:`, `    """${record.name} from ${source}."""`, '']
    for (const constant of record.constants) {
        lines.push(
            ...layoutAssignment(
                INDENT,
                constantName(constant.name, used),
                null,
                atom(pythonString(constant.value)),
            ),
        )
    }
    return lines
}

/**
 * Emits the source lines of a type alias.
 * @param {object} alias Alias record.
 * @returns {string[]} Source lines.
 */
function emitAlias(alias) {
    if (!alias.typeParameters.length)
        return layoutAssignment(0, alias.name, atom('TypeAlias'), alias.value)
    return layoutAssignment(
        0,
        alias.name,
        null,
        callExpression(atom('TypeAliasType'), [
            atom(pythonString(alias.name)),
            alias.value,
            keyword('type_params', tupleExpression(alias.typeParameters.map(atom))),
        ]),
    )
}

/**
 * Emits the whole Python module.
 * @param {object} state Generator state.
 * @returns {{ code: string, summary: { models: number, constants: number, aliases: number } }} Module source and counts.
 */
function emitModule(state) {
    const { source } = state
    const records = state.exports.filter((record) => !record.skipped)
    const constants = records.filter((record) => record.constants)
    const models = topologicalSort(
        records.flatMap((record) => record.classes),
        (model) => atomsOf(model.bases),
    )
    const aliases = orderAliases(
        records.filter((record) => record.alias).map((record) => record.alias),
        models,
    )

    const typeVars = [
        ...new Set([
            ...models.flatMap((model) => model.typeParameters),
            ...aliases.flatMap((alias) => alias.typeParameters),
        ]),
    ].sort(compareText)
    const classNames = new Set([
        ...models.map((model) => model.name),
        ...constants.map((record) => record.name),
    ])
    for (const name of typeVars) {
        if (classNames.has(name) || RUNTIME_NAMES.has(name) || PYTHON_KEYWORDS.has(name)) {
            throw new Error(`type parameter ${name} collides with a generated name`)
        }
    }

    const used = atomsOf([
        ...models.flatMap((model) => [
            ...model.bases,
            ...model.fields.flatMap((field) => [
                field.expression,
                fieldValue(field) ?? atom('None'),
            ]),
        ]),
        ...aliases.map((alias) => alias.value),
    ])
    const typingNames = ['Annotated', 'Any', 'Generic', 'Literal'].filter((name) => used.has(name))
    if (aliases.some((alias) => !alias.typeParameters.length)) typingNames.push('TypeAlias')
    if (typeVars.length) typingNames.push('TypeVar')
    const pydanticNames = ['BaseModel', 'ConfigDict', ...(used.has('Field') ? ['Field'] : [])]
    const needsTypeAliasType = aliases.some((alias) => alias.typeParameters.length)

    const lines = [
        `"""Pydantic models generated from ${source}."""`,
        '',
        'from __future__ import annotations',
        '',
    ]
    if (typingNames.length)
        lines.push(`from typing import ${typingNames.sort(compareText).join(', ')}`, '')
    lines.push(`from pydantic import ${pydanticNames.join(', ')}`)
    if (needsTypeAliasType) lines.push('from typing_extensions import TypeAliasType')
    lines.push('')
    if (typeVars.length) {
        for (const name of typeVars) lines.push(`${name} = TypeVar(${pythonString(name)})`)
        lines.push('')
    }

    const blocks = [
        [
            'class SonolusModel(BaseModel):',
            `    """Base model shared by every ${source} model."""`,
            '',
            ...layoutAssignment(
                INDENT,
                'model_config',
                null,
                callExpression(atom('ConfigDict'), [
                    keyword('populate_by_name', atom('True')),
                    keyword('serialize_by_alias', atom('True')),
                    keyword('extra', atom('"ignore"')),
                ]),
            ),
        ],
        ...[...constants]
            .sort((a, b) => compareText(a.name, b.name))
            .map((record) => emitConstants(record, source)),
        ...models.map((model) => emitModel(model, source)),
    ]
    for (const block of blocks) lines.push('', ...block, '')
    if (aliases.length) lines.push('', ...aliases.flatMap(emitAlias), '')
    if (models.length) {
        lines.push(
            '',
            ...[...models]
                .sort((a, b) => compareText(a.name, b.name))
                .map((model) => `${model.name}.model_rebuild()`),
        )
    }

    return {
        code: `${lines.join('\n').replace(/\n{4,}/g, '\n\n\n')}\n`,
        summary: { models: models.length, constants: constants.length, aliases: aliases.length },
    }
}

main()
