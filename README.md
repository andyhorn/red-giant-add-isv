# Red Giant - Add ISV
A simple Python command-line tool to add a static ISV port to Red Giant RLM licenses.

## Usage
`usage: add-isv.py [-h] [-o OUT ] [-l | -z] -d DIR -p PORT`

### Optional Arguments
| flag | action |
| --- | --- |
| -h, --help | Show the help message |
| -o OUT, --out OUT | Save modified files to a different output directory
| -l, --lic | Directly modify license (.lic) files |
| -z, --zip | Modify server license files within .zip files |

### Required Arguments
| flag | action |
| --- | --- |
| -d DIR, --dir DIR | The directory containing the license file(s) |
| -p PORT, --port PORT | The ISV port value to add to each file |


### Examples
#### Inject ISV into .zip file, overwriting existing files
`python add-isv.py -z -p 5055 -d /path/to/directory`

#### Inject ISV into .lic files, overwriting existing files
`python add-isv.py -l -p 5055 -d /path/to/directory`

#### Inject ISV into .zip files, preserving original files
`python add-isv.py -z -p 5055 -d /path/to/directory -o /path/to/output/directory`

