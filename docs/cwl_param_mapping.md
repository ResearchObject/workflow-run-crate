# CWL parameter mapping

## Type mappings

### string

Map to [Text](http://schema.org/Text).

```json
{
    "@id": "#param/in_str",
    "@type": "FormalParameter",
    "additionalType": "Text",
    "name": "in_str"
},
{
    "@id": "#pv/in_str",
    "@type": "PropertyValue",
    "exampleOfWork": {"@id": "#param/in_str"},
    "name": "in_str",
    "value": "spam"
}
```

### array

A property in RO-Crate can have a single value or multiple values, so the `additionalType` can simply be the mapping of the element's type (e.g., `string[]` to [Text](http://schema.org/Text)). To register the fact that the workflow allows multiple entries for that parameter, set [multipleValues](http://schema.org/multipleValues) to [True](http://schema.org/True):

```json
{
    "@id": "#param/in_array",
    "@type": "FormalParameter",
    "additionalType": "Text",
    "multipleValues": "True",
    "name": "in_array"
},
{
    "@id": "#pv/in_array",
    "@type": "PropertyValue",
    "exampleOfWork": {"@id": "#param/in_array"},
    "name": "in_array",
    "value": ["foo", "bar"]
}
```

This reuses `multipleValues` from [PropertyValueSpecification](https://schema.org/PropertyValueSpecification), similarly to what [FormalParameter](https://bioschemas.org/types/FormalParameter/1.0-RELEASE) does for `defaultValue` and `valueRequired`.

### Any

Map to [DataType](http://schema.org/DataType).

```json
{
    "@id": "#param/in_any",
    "@type": "FormalParameter",
    "additionalType": "DataType",
    "name": "in_any"
},
{
    "@id": "#pv/in_any",
    "@type": "PropertyValue",
    "exampleOfWork": {"@id": "#param/in_any"},
    "name": "in_any",
    "value": "tar"
}
```

### boolean

Map to [Boolean](http://schema.org/Boolean).

```json
{
    "@id": "#param/in_bool",
    "@type": "FormalParameter",
    "additionalType": "Boolean",
    "name": "in_bool"
},
{
    "@id": "#pv/in_bool",
    "@type": "PropertyValue",
    "exampleOfWork": {"@id": "#param/in_bool"},
    "name": "in_bool",
    "value": "True"
}
```

### int, long

Map to [Integer](http://schema.org/Integer).

```json
{
    "@id": "#param/in_int",
    "@type": "FormalParameter",
    "additionalType": "Integer",
    "name": "in_int"
},
{
    "@id": "#pv/in_int",
    "@type": "PropertyValue",
    "exampleOfWork": {"@id": "#param/in_int"},
    "name": "in_int",
    "value": "42"
}
```

### float, double

Map to [Float](http://schema.org/Float).

```json
{
    "@id": "#param/in_float",
    "@type": "FormalParameter",
    "additionalType": "Float",
    "name": "in_float"
},
{
    "@id": "#pv/in_float",
    "@type": "PropertyValue",
    "exampleOfWork": {"@id": "#param/in_float"},
    "name": "in_float",
    "value": "3.14"
}
```

### multiple types

Map to array of mappings of each type, e.g., `[int, float]` to `["Integer", "Float"]`. Note that the CWL type array may include `"null"`, indicating that the parameter is optional (and should have a default value): in this case, set [valueRequired](http://schema.org/valueRequired) to [False](http://schema.org/False):

```json
{
    "@id": "#param/in_multi",
    "@type": "FormalParameter",
    "additionalType": ["Float", "Integer"],
    "defaultValue": "9.99",
    "name": "in_multi",
    "valueRequired": "False"
},
{
    "@id": "#pv/in_multi",
    "@type": "PropertyValue",
    "exampleOfWork": {"@id": "#param/in_multi"},
    "name": "in_multi",
    "value": "9.99"
} 
```

### enum

Map to [Text](http://schema.org/Text). The set of predefined allowed values can be represented via [valuePattern](http://schema.org/valuePattern):

```json
{
    "@id": "#param/in_enum",
    "@type": "FormalParameter",
    "additionalType": "Text",
    "name": "in_enum",
    "valuePattern": "A|B"
},
{
    "@id": "#pv/in_enum",
    "@type": "PropertyValue",
    "exampleOfWork": {"@id": "#param/in_enum"},
    "name": "in_enum",
    "value": "B"
}
```

### record

Map to [PropertyValue](http://schema.org/PropertyValue). It actually maps to an array of `PropertyValue`s, so [multipleValues](http://schema.org/multipleValues) can be set to [True](http://schema.org/True) (similarly to the mapping of `array`). To serialize the actual value of `{"in_record_A": "Tom", "in_record_B": "Jerry"}`, use nested `PropertyValue`s:


```json
{
    "@id": "#param/in_record",
    "@type": "FormalParameter",
    "additionalType": "PropertyValue",
    "multipleValues": "True",
    "name": "in_record"
},
{
    "@id": "#pv/in_record",
    "@type": "PropertyValue",
    "exampleOfWork": {"@id": "#param/in_record"},
    "name": "in_record",
    "value": [
        {"@id": "#pv/in_record/in_record_A"},
        {"@id": "#pv/in_record/in_record_B"}
    ]
}
{
    "@id": "#pv/in_record/in_record_A",
    "@type": "PropertyValue",
    "name": "in_record/in_record_A",
    "value": "Tom"
},
{
    "@id": "#pv/in_record/in_record_B",
    "@type": "PropertyValue",
    "name": "in_record/in_record_B",
    "value": "Jerry"
},
```

In the above example, record keys have been used to set additional slash-separated fields in the `@id`.


## Annotations

### format

Use [FormalParameter](https://bioschemas.org/types/FormalParameter/1.0-RELEASE)'s `encodingFormat`:

```json
{
    "@id": "#param/input",
    "@type": "FormalParameter",
    "additionalType": "File",
    "encodingFormat": "https://www.iana.org/assignments/media-types/text/csv",
    "name": "input"
}
```
