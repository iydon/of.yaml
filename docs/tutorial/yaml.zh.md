# YAML 速查表

## 入门

### 简介

[YAML](https://github.com/yaml/) 是一个可读性高，用来表达资料序列化的格式。

- YAML 不允许使用制表符；
-  元素部分之间必须有空格；
- YAML 是区分大小写的；
- YAML 文件的拓展名为 `.yaml` 或 `.yml`；
- YAML 是 JSON 的超集。


### 标量

YAML 使用空格来缩进，元素部分之间必须有空格。

=== "YAML"
    ```yaml
    n1: 1            # integer
    n2: 1.234        # float

    s1: 'abc'        # string
    s2: "abc"        # string
    s3: abc          # string

    b: false         # boolean type

    d: 2015-04-05    # date type
    ```
=== "JSON"
    ```json
    {
        "n1": 1,
        "n2": 1.234,
        "s1": "abc",
        "s2": "abc",
        "s3": "abc",
        "b": false,
        "d": "2015-04-05"
    }
    ```


### 变量

=== "YAML"
    ```yaml
    some_thing: &VAR_NAME foobar
    other_thing: *VAR_NAME
    ```
=== "JSON"
    ```json
    {
        "some_thing": "foobar",
        "other_thing": "foobar"
    }
    ```


### 注释

=== "YAML"
    ```yaml
    # A single line comment example

    # block level comment example
    # comment line 1
    # comment line 2
    # comment line 3
    ```


### 继承

=== "YAML"
    ```yaml
    parent: &defaults
        a: 2
        b: 3

    child:
        <<: *defaults
        b: 4
    ```
=== "JSON"
    ```json
    {
        "parent": {
            "a": 2,
            "b": 3
        },
        "child": {
            "a": 2,
            "b": 4
        }
    }
    ```


### 引用

=== "YAML"
    ```yaml
    values: &ref
        - Will be
        - reused below

    other_values:
        i_am_ref: *ref
    ```
=== "JSON"
    ```json
    {
        "values": [
            "Will be",
            "reused below"
        ],
        "other_values": {
            "i_am_ref": [
                "Will be",
                "reused below"
            ]
        }
    }
    ```


### 多行字符串

=== "YAML"
    ```yaml
    description: |
        hello
        world
    ```
=== "JSON"
    ```json
        {"description": "hello\nworld\n"}
    ```


### 折叠字符串

=== "YAML"
    ```yaml
    description: >
        hello
        world
    ```
=== "JSON"
    ```json
    {"description": "hello world\n"}
    ```


### 多文档

YAML 使用 `---` 来分隔多文档内容。

=== "YAML"
    ```yaml
    ---
    document: this is doc 1
    ---
    document: this is doc 2
    ```



## 集合

### 序列

=== "YAML"
    ```yaml
    - Mark McGwire
    - Sammy Sosa
    - Ken Griffey
    ```
=== "JSON"
    ```json
    [
        "Mark McGwire",
        "Sammy Sosa",
        "Ken Griffey"
    ]
    ```


### 映射

=== "YAML"
    ```yaml
    hr:  65       # Home runs
    avg: 0.278    # Batting average
    rbi: 147      # Runs Batted In
    ```
=== "JSON"
    ```json
    {
        "hr": 65,
        "avg": 0.278,
        "rbi": 147
    }
    ```


### 映射到序列上

=== "YAML"
    ```yaml
    attributes:
        - a1
        - a2
    methods: [getter, setter]
    ```
=== "JSON"
    ```json
    {
        "attributes": ["a1", "a2"],
        "methods": ["getter", "setter"]
    }
    ```


### 映射的序列

=== "YAML"
    ```yaml
    children:
        - name: Jimmy Smith
          age: 15
        - name: Jimmy Smith
          age: 15
        -
            name: Sammy Sosa
            age: 12
    ```
=== "JSON"
    ```json
    {
        "children": [
            {"name": "Jimmy Smith", "age": 15},
            {"name": "Jimmy Smith", "age": 15},
            {"name": "Sammy Sosa", "age": 12}
        ]
    }
    ```


### 序列的序列

=== "YAML"
    ```yaml
    my_sequences:
        - [1, 2, 3]
        - [4, 5, 6]
        -
            - 7
            - 8
            - 9
            - 0
    ```
=== "JSON"
    ```json
    {
        "my_sequences": [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9, 0]
        ]
    }
    ```


### 映射到映射上

=== "YAML"
    ```yaml
    Mark McGwire: {hr: 65, avg: 0.278}
    Sammy Sosa: {
        hr: 63,
        avg: 0.288
    }
    ```
=== "JSON"
    ```json
    {
        "Mark McGwire": {
            "hr": 65,
            "avg": 0.278
        },
        "Sammy Sosa": {
            "hr": 63,
            "avg": 0.288
        }
    }
    ```


### 嵌套集合

=== "YAML"
    ```yaml
    Jack:
        id: 1
        name: Franc
        salary: 25000
        hobby:
            - a
            - b
        location: {country: "A", city: "A-A"}
    ```
=== "JSON"
    ```json
    {
        "Jack": {
            "id": 1,
            "name": "Franc",
            "salary": 25000,
            "hobby": ["a", "b"],
            "location": {
                "country": "A", "city": "A-A"
            }
        }
    }
    ```



## 参考

- [github.com/Randy8080/reference](https://github.com/Randy8080/reference/blob/main/yaml.md)
