import ply.lex as lex
from src.lexer.token import Token
from typing import List
from src.change.line import Line

"""
This file contains the rules and token type definitions for the lexer (ply library). The library function
token() will extract the tokens from a single code line based on the types defined in this file.
The list called <reserved> stores all the C/C++ keywords, while list called <tokens> will specify the
symbols used in those languages, and will include the <reserved> list.
"""

reserved = {
    'alignas': 'ALIGNAS',
    'alignof': 'ALIGNOF',
    'and': 'AND',
    'and_eq': 'ANDEQ',
    'asm': 'ASM',
    'atomic_cancel': 'ATOMIC_CANCEL',
    'atomic_commit': 'ATOMIC_COMMIT',
    'atomic_noexcept': 'ATOMIC_NOEXCEPT',
    'auto': 'AUTO',
    'bitand': 'BITAND',
    'bitor': 'BITOR',
    'bool': 'BOOL',
    'break': 'BREAK',
    'case': 'CASE',
    'catch': 'CATCH',
    'char': 'CHAR',
    'char8_t': 'CHAR_8T',
    'char16_t': 'CHAR_16T',
    'char32_t': 'CHAR_32T',
    'class': 'CLASS',
    'compl': 'COMPL',
    'concept': 'CONCEPT',
    'const': 'CONST',
    'consteval': 'CONSTEVAL',
    'constexpr': 'CONSTEXPR',
    'constint': 'CONSTINT',
    'const_cast': 'CONST_CAST',
    'continue': 'CONTINUE',
    'cout': 'COUT',
    'cin': 'CIN',
    'co_await': 'CO_AWAIT',
    'co_return': 'CO_RETURN',
    'co_yield': 'CO_YIELD',
    'decltype': 'DECLTYPE',
    'default': 'DEFAULT',
    'delete': 'DELETE',
    'do': 'DO',
    'double': 'DOUBLE',
    'dynamic_cast': 'DYNAMIC_CAST',
    'else': 'ELSE',
    'endl': 'ENDL',
    'enum': 'ENUM',
    'explicit': 'EXPLICIT',
    'export': 'EXPORT',
    'extern': 'EXTERN',
    'false': 'FALSE',
    'float': 'FLOAT',
    'for': 'FOR',
    'friend': 'FRIEND',
    'goto': 'GOTO',
    'if': 'IF',
    'include': 'INCLUDE',
    'inline': 'INLINE',
    'int': 'INT',
    'long': 'LONG',
    'mutable': 'MUTABLE',
    'namespace': 'NAMESPACE',
    'new': 'NEW',
    'noexcept': 'NOEXCEPT',
    'not': 'NOT',
    'not_eq': 'NOT_EQ',
    'NULL': 'NULL',
    'nullptr': 'NULLPTR',
    'operator': 'OPERATOR',
    'or': 'OR',
    'or_eq': 'OR_EQ',
    'private': 'PRIVATE',
    'protected': 'PROTECTED',
    'public': 'PUBLIC',
    'reflexpr': 'REFLEXEPR',
    'register': 'REGISTER',
    'reinterpret_cast': 'REINTERPRET_CAST',
    'requires': 'REQUIRES',
    'return': 'RETURN',
    'short': 'SHORT',
    'signed': 'SIGNED',
    'sizeof': 'SIZEOF',
    'static': 'STATIC',
    'static_assert': 'STATIC_ASSERT',
    'static_cast': 'STATIC_CAST',
    'string': 'STRING',
    'struct': 'STRUCT',
    'switch': 'SWITCH',
    'synchronized': 'SYNCHRONIZED',
    'template': 'TEMPLATE',
    'this': 'THIS',
    'thread_local': 'THREAD_LOCAL',
    'throw': 'THROW',
    'true': 'TRUE',
    'try': 'TRY',
    'typedef': 'TYPEDEF',
    'typeid': 'TYPEID',
    'typename': 'TYPENAME',
    'union': 'UNION',
    'unsigned': 'UNSIGNED',
    'using': 'USING',
    'virtual': 'VIRTUAL',
    'void': 'VOID',
    'volatile': 'VOLATILE',
    'wchar_t': 'WCHAR_T',
    'while': 'WHILE',
    'xor': 'XOR',
    'xor_eq': 'XOR_EQ'
}

tokens = [
    'ID',
    'COMMENT',
    'NUMBER',
    'COMMENTINLINE',
    'COMMENTSTART',
    'COMMENTEND',
    'PLUS',
    'MINUS',
    'MUL',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'LSQPAREN',
    'RSQPAREN',
    'LCURPAREN',
    'RCURPAREN',
    'END',
    'COMMA',
    'EQUAL',
    'PLUSEQUAL',
    'MINUSEQUAL',
    'TIMESEQUAL',
    'ISEQUAL',
    'GREATER',
    'LOWER',
    'GREATEROREQUAL',
    'LOWEROREQUAL',
    'DIFFERENT',
    'REMAINDER',
    'QUOTE',
    'SMALLQUOTE',
    'AMP',
    'CARR',
    'DOT',
    'HASH',
    'SEP',
    'NEG',
    'BACKSLASH',
    'QUESTMARK',
    'POINTS',
    'ELSEIF',
    'AT',
    'UPARROW',
    'TILDE',
    'TILDE_2',
    'DOLLAR'
] + list(reserved.values())

t_PLUS = r'\+'
t_MINUS = r'\-'
t_MUL = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LSQPAREN = r'\['
t_RSQPAREN = r'\]'
t_LCURPAREN = r'\{'
t_RCURPAREN = r'\}'
t_END = r'\;'
t_COMMA = r'\,'
t_EQUAL = r'\='
t_PLUSEQUAL = r'\+='
t_MINUSEQUAL = r'\-='
t_TIMESEQUAL = r'\*='
t_ISEQUAL = r'\=='
t_GREATER = r'\>'
t_LOWER = r'\<'
t_GREATEROREQUAL = r'\>='
t_LOWEROREQUAL = r'\<='
t_DIFFERENT = r'\!='
t_REMAINDER = r'\%'
t_QUOTE = r'\"'
t_SMALLQUOTE = r'\''
t_AMP = r'\&'
t_CARR = r'\\n|\\r|\\t'
t_DOT = r'\.'
t_HASH = r'\#'
t_SEP = r'\|'
t_NEG = r'\!'
t_BACKSLASH = r'\\'
t_QUESTMARK = r'\?'
t_POINTS = r'\:'
t_ELSEIF = r'^else\sif'
t_COMMENTINLINE = r'\/\/'
t_COMMENTSTART = r'\/\*'
t_COMMENTEND = r'\*\/'
t_AT = r'\@'
t_UPARROW = r'\^'
t_TILDE = r'\`'
t_TILDE_2 = r'\~'
t_DOLLAR = r'\$'
t_ignore = ' \t'


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()


def extract_tokens(line: str) -> List[Line]:
    lexer.input(line)
    tokens = []

    while True:
        token = lexer.token()

        if not token:
            break

        tokens.append(Token(token.type, token.value))

    return tokens
