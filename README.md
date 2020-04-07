# Red Giant - Add ISV
A simple Python command-line tool to add a static ISV port to Red Giant RLM licenses.

## Usage
`usage: add-isv.py [-h] [-o OUT ] (-l | -z) -p PORT path`

### Optional Arguments
| flag | action |
| --- | --- |
| -h, --help | Show the help message |
| -o OUT, --out OUT | specify a different output path for the modified file(s); default will overwrite
| -d, --dir | a directory of files to modify |

### Required Arguments
| flag | action |
| --- | --- |
| -p PORT, --port PORT | the ISV port to add to each file |
| -l, --lic | modify .lic files |
| -z, --zip | modify full .zip files |


### Examples
#### Inject ISV into .zip file, overwriting existing files
`python add-isv.py -z -p 5055 /path/to/file.zip`

#### Inject ISV into .lic files, overwriting existing files
`python add-isv.py -l -p 5055 /path/to/file.lic`

#### Inject ISV into multiple .zip files, preserving original files
`python add-isv.py -z -d -p 5055 -o /path/to/output/directory /path/to/directory`

#### Inject ISV into one file, preserving original file
`python add-isv.py -l -p 5055 -o /path/to/new/file.lic /path/to/file.lic`