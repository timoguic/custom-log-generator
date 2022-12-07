# Dolos, a custom log generator <!-- omit from toc -->

- [Installation](#installation)
- [Usage](#usage)
  - [For now](#for-now)
  - [Later](#later)
- [Providers](#providers)
  - [User provider](#user-provider)
  - [Time provider](#time-provider)
- [Pattern](#pattern)
- [Fields](#fields)
  - [Static data field](#static-data-field)
  - [Function field](#function-field)
    - [List of builtin `func`s](#list-of-builtin-funcs)
  - [User provider field](#user-provider-field)
    - [Time provider field](#time-provider-field)
  - [Template provider field](#template-provider-field)

# Installation

* Create a virtual environment: `python -m venv venv` (creates a virtual environment in the `venv` folder)
* Activate the virtual environment:
  * `source venv/bin/activate` on macOS / Linux
  * `.\venv\Scripts\activate` on Windows
* git clone the repository
* install the dependencies **in the virtual environment** (make sure it's active): `pip install -r requirements.txt`

# Usage

## For now
* Create / modify the configuration file `config.yaml`
* Run the script: `python cli.py --config config.yaml`

## Later

The package has one command, `dolos_generate`, that can be run from the command line.

# Providers

## User provider

Configure the user provider by setting the `users` section of the configuration file. A typical user section looks like:

```yaml
users:
  count: 100
  fields:
    name:
      func: name
    ip_address:
      generator: ipv4
      cidr_range: "172.16.0.0./12"
      excluded: ["172.16.0.1", "172.16.0.254"]
  save_to: users.json
```

* `count`: the number of users to generate
* `fields`: the fields that make up the user "model" (see below)
* `save_to` (optional): if provided, the generated users will be saved to this file in JSON format 

## Time provider

Configure the time provider by setting the `timestamps` section of the configuration file. A typical configuration looks like:

```yaml
timestamps:
  start: 2022-12-02 10:00
  interval: 3
```

* `start`: the start date / time for log generation
* `interval`: the number of seconds between each log entry

# Pattern

The configuration file must contain a `pattern`. A pattern is a string - it can contain $-variables that will be substituted when generating the log entries.

```yaml
pattern: "$name $time 172.16.0.1 CEF:0|Forcepoint|Security| app=http dvc=$src_ip dst=172.16.0.1 dpt=80 src=192.0.2.4 spt=$src_port $request_data"
```

Each $-variable must be defined in the corresponding `fields` section.

# Fields

Fields either hold or generate the data that will be substituted in the pattern. A field can be of several types:
* associated to a provider
* associated to a function
* associated to static data

## Static data field

Simply define the value of the field in the `data` attribute:

```yaml
fields:
  test:
    data: "Hello world!"
```
## Function field

A function field is identified by its `func` attribute, which refers to the Python function executed when rendering the field.

* if `func` contains a Python-dotted path, it will be imported accordingly (it must be an absolute import)
* if `func` is a string without dots, it will be looked up in the `generators` package of the application
* other attributes are passed as keyword arguments to the function upon rendering

Example:

```yaml
fields:
  src_port:
    func: randint
    min: 2048
    max: 16000
  request_data:
    func: generators.custom.request
```

`src_port` will be generated using the `randint` builtin function.
`request_data` will be generated using the function `request` located in the Python module `generators.custom`.

### List of builtin `func`s

| Name        | Behaviour                               | Keyword arguments                                                  |
| ----------- | --------------------------------------- | ------------------------------------------------------------------ |
| `randint`   | Returns a random integer                | `min` (required): minimum value<br>`max` (required): maximum value |
| `name`      | Returns a random name                   | None                                                               |
| `from_file` | Returns a random line out of a file     | `filename`: path to the file to read from                          |
| `from_list` | Returns a random element from of a list | `values`: list of values to choose from                            |

## User provider field

```yaml
fields:
  name:
    provider: user
    attribute: name
```

The `attribute` must be the name of a field defined in the user provider configuration.

### Time provider field

```yaml
fields:
  time:
    provider: timestamp
    format: "%b %d %H:%M:%S"
```

The `format` is a string representing the [date/time format](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes).

## Template provider field

The template provider allows to create "atomic" blocks in the log line. It works exactly like the main `pattern` declaration.
Use `provider: template`, define the `pattern` and the `fields`.

```yaml
pattern: "firewall traffic $something"      # "main" pattern
fields:
  something:
    provider: template
    pattern: "user=$name in=$in out=$out"   # sub-pattern
    fields:
      name:
        func: name
      in:
        func: randint
        min: 10
        max: 15
      out:
        func: randint
        min: 1000
        max: 1500
```


# Why `dolos`? <!-- omit from toc -->
The original purpose of the project is to generate large amount of logs, where one can then inject suspicious traffic patterns. Students in IT security then have to identify and detect malicious traffic / users.

In Greek mythology, [Dolos](https://en.wikipedia.org/wiki/Dolos_(mythology)) is the spirit of trickery.


This project was supported by [OpenClassrooms](https://openclassrooms.com/).