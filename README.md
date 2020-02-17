# drawdiff
It is an beta-version of my project which provides capability to highlight difference between two versions of Draw.io diagram. This tool is not about real diff like in git but rather just to help people to find changes between versions.
It supports two modes: comparison of local files and Confluence integration.

## Usage
Clone this project then   
`cd drawdiff`

### Local mode
Compares two files stored locally and creates the third file with highlighted changes.

```bash
python ./main.py -l ./examples/test1_1.xml ./examples/test1_2.xml -o output.xml
```

### Confluence mode
Firstly you need to specify confluence configuration. To do this create 'drawdiff_conf.json' in a project root directory.
You can find template of the file [here](./drawdiff_conf_template.json). In this mode drawdiff will download specified versions of diagram attached to the page and compare them without saving file locally. If there are more than one diagram in attachments drawdiff will ask you to specify a name of diagram
'title' field is not mandatory and is for development purpose.

```bash
python main.py -t <page_title> version_number1 version_number2 -o output.xml
```
## Examples
You can find examples [here](./examples/README.md)
