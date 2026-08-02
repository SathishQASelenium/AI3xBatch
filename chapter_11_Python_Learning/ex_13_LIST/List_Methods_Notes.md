# Summary of List Methods

## 1. `append()`
Add single item to end of list.
```python
fruits = ["apple", "banana"]
fruits.append("mango")
print(fruits)  # ['apple', 'banana', 'mango']
```

## 2. `extend()`
Add all items of another iterable to end of list.
```python
fruits = ["apple", "banana"]
fruits.extend(["mango", "grape"])
print(fruits)  # ['apple', 'banana', 'mango', 'grape']
```

## 3. `insert()`
Insert item at given index (shifts rest right).
```python
fruits = ["apple", "banana"]
fruits.insert(1, "kiwi")
print(fruits)  # ['apple', 'kiwi', 'banana']
```

## 4. `remove()`
Remove first matching value. Raises `ValueError` if not found.
```python
fruits = ["apple", "banana", "apple"]
fruits.remove("apple")
print(fruits)  # ['banana', 'apple']
```

## 5. `pop()`
Remove and return item at index (default last).
```python
fruits = ["apple", "banana", "mango"]
last = fruits.pop()
print(last)    # mango
print(fruits)  # ['apple', 'banana']

first = fruits.pop(0)
print(first)   # apple
```

## 6. `clear()`
Remove all items, list becomes empty.
```python
fruits = ["apple", "banana"]
fruits.clear()
print(fruits)  # []
```

## 7. `index()`
Return index of first matching value. Raises `ValueError` if not found.
```python
fruits = ["apple", "banana", "mango"]
print(fruits.index("banana"))  # 1
```

## 8. `count()`
Count occurrences of value in list.
```python
marks = [90, 91, 90, 78, 90]
print(marks.count(90))  # 3
```

## 9. `sort()`
Sort list in place (ascending by default).
```python
marks = [90, 78, 92, 56]
marks.sort()
print(marks)  # [56, 78, 90, 92]

marks.sort(reverse=True)
print(marks)  # [92, 90, 78, 56]
```

## 10. `reverse()`
Reverse order of items in place.
```python
fruits = ["apple", "banana", "mango"]
fruits.reverse()
print(fruits)  # ['mango', 'banana', 'apple']
```

## 11. `copy()`
Return shallow copy of list (independent object, safe from mutation of original).
```python
fruits = ["apple", "banana"]
fruits_copy = fruits.copy()
fruits_copy.append("mango")
print(fruits)       # ['apple', 'banana']
print(fruits_copy)  # ['apple', 'banana', 'mango']
```
