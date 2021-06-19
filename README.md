# Null Safe Python

Null safe support for Python.

## Installation

```bash
pip install nullsafe
```

## Quick Start

Dummy Class

```python
class Dummy:
    pass
```

Normal Python code:

```python
o = Dummy()

try:
    value = o.inexistent
    print("accessed")
except AttributeError:
    value = None
```

With nullsafe:

```python
from nullsafe import undefined, _

o = Dummy()

value = _(o).inexistent

if value is not undefined:
    print("accessed")
```

# Documentation

## Basics

There are 5 values importable in nullsafe root:

### class `NullSafeProxy: (o: T)`

Receives an object `o` on instantiation.

Proxy class for granting nullsafe abilities to an object.

### class `NullSafe: ()`

No argument needed.

Nullish class with with nullsafe abilities. Instances will have a falsy boolean evaluation, equity comparison (`==`) to `None` and instance of `NullSafe` returns `True`, otherwise `False`. Identity comparison (`is`) to `None` will return `False`.

### variable `undefined: NullSafe`

Instance of `Nullsafe`, this instance will be returned for all nullish access in a proxied object, enabling identity comparison `value is undefined` for code clarity.

### function `nullsafe: (o: T) -> T`

Receives an object `o` as argument.

Helper function that checks if object is nullish and return the proxied object.

return `undefined` if `o` is `None` or `undefined`, otherwise return the proxied object `NullSafeProxy[T]`.

This function is **generic typed** (`(o: T) -> T`), code autocompletions and linters functionalities will remain. Disclaimer: If the object was not typed before proxy, it obviously won't come out typed out of the blue.

### function `_: (o: T) -> T` (alias to `nullsafe`)

Alias to `nullsafe`, used for better code clarity.

The examples shown will be using `_` instead of `nullsafe` for code clarity. For better understanding, the Javascript equivalents will be shown as comments.

## Implementation

Nullsafe abilities are granted after proxying an object through `NullSafeProxy`. To proxy an object pass it through `_()` or `nullsafe()`. Due to language limitation, the implementation does not follow the "return the first nullish value in chain", instead it "extend the a custom nullish value until the end of chain". Inexistent values of a proxied object and its subsequent values in chain will return `undefined`.

## Import

```python
from nullsafe import undefined, _
```

## Usage

There are various way to get a nullsafe proxied object.

### Null safe attribute access

Proxied object doing a possibly `AttributeError` access.

```python
o = Dummy()

# o.inexistent
assert _(o).inexistent is undefined
assert _(o).inexistent == None   # undefined == None
assert not _(o).inexistent       # bool(undefined) == False

# o.inexistent?.nested
assert _(o).inexistent.nested is undefined

# o.existent.inexistent?.nested
assert _(o.existent).inexistent.nested is undefined

# o.maybe?.inexistent?.nested
assert _(_(o).maybe).inexistent.nested is undefined
```

### Null safe item access

Proxied object doing a possibly `KeyError` access.

```python
o = Dummy() # dict works too !

# o.inexistent
assert _(o)["inexistent"] is undefined
assert _(o)["inexistent"] == None    # undefined == None
assert not _(o)["inexistent"]        # bool(undefined) == False

# o.inexistent?.nested
assert _(o)["inexistent"]["nested"] is undefined

# o.existent.inexistent?.nested
assert _(o["existent"])["inexistent"]["nested"] is undefined

# o.maybe?.inexistent?.nested
assert _(_(o)["maybe"])["inexistent"]["nested"] is undefined
```

### Null safe post evaluation

Possibly `None` or `undefined` object doing possibly `AttributeError` or `KeyError` access.

Note: This only works if the seeking value is accessible, see [limitations](#post-evaluation)

```python
o = Dummy() # dict works too !
o.nay = None

# o.nay?.inexistent
assert _(o.nay).inexistent is undefined
assert _(o.nay).inexistent == None   # undefined == None
assert not _(o.nay).inexistent       # bool(undefined) == False

# o.nay?.inexistent.nested
assert _(o.nay).inexistent.nested is undefined
```

```python
o = Dummy() # dict works too !
o["nay"] = None

# o.nay?.inexistent
assert _(o["nay"])["inexistent"] is undefined
assert not _(o["nay"])["inexistent"]

# o.nay?.inexistent.nested
assert _(o["nay"])["inexistent"]["nested"] is undefined
assert not _(o["nay"])["inexistent"]["nested"]
```

### Combined usage

Of course you can combine different styles.

```python
assert _(o).inexistent["inexistent"].inexistent.inexistent["inexistent"]["inexistent"] is undefined
```

## Limitations

List of limitations that you may encounter.

### `undefined` behavior

`undefined` is actually an instance of `NullSafe`, the actual mechanism used for nullsafe chaining, it cannot self rip the nullsafe functionality when the chain ends (because it doesn't know), so this following actually possible and probably not the wanted behavior.

```python
val = _(o).inexistent

assert val.another_inexistent is undefined
```

### Post evaluation

In other languages like Javascript, it checks for each item in the chain and return `undefined` on the first nullish value, which in fact is post-evaluated. This is not possible in python because it raises an `AttributeError` or `KeyError` on access attempt, unless it returns `None` (see [one of the available usage](#null-safe-post-evaluation)), so it must proxy the instance that may contain the attr or key before accessing.

```python
try:
    val = _(o.inexistent).nested # AttributeError: '<type>' object has no attribute 'inexistent'
except AttributeError:
    assert True
assert _(o).inexistent.nested is undefined
```

## Contributing

Contributions welcomed ! Make sure it passes current tests tho.

