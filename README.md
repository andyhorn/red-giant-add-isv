# Red Giant - Add ISV
A simple Python command-line tool to add a static ISV port to Red Giant RLM licenses.

## Usage
`usage: add-isv.py [-h] [-l | -z] -d DIR -p PORT`

### Optional Arguments
| flag | action |
| --- | --- |
| -h, --help | Show the help message |
| -l, --lic | Directly modify license (.lic) files |
| -z, --zip | Modify server license files within .zip files |

### Required Arguments
| flag | action |
| --- | --- |
| -d DIR, --dir DIR | The directory containing the license file(s) |
| -p PORT, --port PORT | The ISV port value to add to each file |
