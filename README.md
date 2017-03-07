# condconf
Generate condition functions from configuration files.

## Usage
The condition functions will be genereated throught the following tempalte

```python
{decorators}
def {function_name}({function_args}):
    {preprocess_code}
    if {true_condition}:
        return True
    else:
        return False
```

The `{}` parts (excpet `true_condition` which is genereated through function configurations) above should be filled in as the following sample code.

### Example

```python
import json

from condconf import cond_func_generator, CondMeta


# Function to be send to condconf
def log_text(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        logger.info(args[0])
        return result
    return wrapper

# Configuration of condition functions
condition_config = [
	{
		"name": "is_greeting",
		"condition": {
			"type": "complex-all",
			"content": [
				{
					"type": "any",
					"content": ["hi", "hello"]
				},
				{
					"type": "any",
					"content": ["there"]
				}
			]
		}
	},
	{
		"name": "is_goodbye",
		"condition": {
			"type": "all",
			"content": ["good", "bye"]
	} 
]

# Arguments of condition functions
template_args = {
	'decorators': ['log_text'],
	'func_args': ['self', 'text'],
	'preprocess_code': ['msg = text.strip()']
}

# Variables needed in condition functions
external_globals = {
	'log_text': log_text
}

# Generate Condition Function Codes
cond_funcs = cond_func_generator(
	condition_config,
	template_args=template_args,
	cond_var_name='msg'
)

# Generate Condition Functions in class through metaclass
class CondCls(metaclass=CondMeta, cond_funcs=cond_funcs, external_globals=external_globals):
	pass
```

The class would be generated as follow

```python
class CondCls(base_classes):
	@log_text
	def is_greeting(self, text):
    msg = text.strip()
    if any(tmp in msg for tmp in ['hi', 'hello']) and any(tmp in msg for tmp in ['there']):
        return True
    else:
        return False
        
	@log_text
	def is_goodbye(self, text):
		msg = text.strip()
		if all(tmp in msg for tmp in ['good', 'bye']):
			return True
		else:
			return False
```

`cond_var_name` in `cond_func_generator` should be the variable used in condition judgement.

## Configs

### template_args
Common setting of these condition functions

- decorators (List[str]): Decorators
- func_args (List[Str]): Function Arguments
- preprocess_code (List[Str]): Each line should be an element of this list  
  (e.g. `["msg = text.strip()", "msg = msg.upper()"]`)

### external_globals
Sometimes these condition functions might contain libraries or user defined functions.  
They should be pass into `CondMeta`.

e.g.

```python
import os

external_globals = {'os': os}
```

### condition_config
List of function configurations.

```json
[
	{
		"name": "is_greeting",
		"condition": {
			"type": "complex-all",
			"content": [
				{
					"type": "any",
					"content": ["hi", "hello"]
				},
				{
					"type": "any",
					"content": ["there"]
				}
			]
		}
	},
	{
		"name": "is_goodbye",
		"condition": {
			"type": "all",
			"content": ["good", "bye"]
	} 
]

```

Function should have the following attributes

- name: function name
- [condition](#condtype): 
	- type: Currentyly support `any`, `all`, `match`, `complex-any`, `complex-all` 
	- content: keywords or condition 

### <a name="condtype"></a> Condition Types
#### any
- content: List of keywords

If any of keywords is in cond_var_name, the function returns True.

#### all
- content: List of keywords	

If all of keywords is in cond_var_name, then the function returns True.

#### match
- content: List of keywords

If cond_var_name matches any of keywords in content, the function returns True.

#### complex-any
- content: List of condition

If any of conditions returns True, the function returns True.

#### complex-all
- content: List of condition

If all of conditions returns True, the function returns True.


# AUTHORS
[Lee-W](https://github.com/Lee-W/)

# License
MIT
