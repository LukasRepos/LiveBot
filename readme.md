# Live bot development guide

## How to use and modify
First, there must be an XML configuration file, [*see here the documentation*](#documentation), to contain all the
rules for the chatbot. The files under the configuration folder and the `main.py` are just files used for testing
and therefore are not essencial to the core of the chatbot and can be safetely removed.
To initalize the bot, all that is needed is to create an instance of the class `CognitiveFunction` and call the method
`process_language` on it passing the input document and it will return a string containing the answer.

## Documentation
It is mandatory a *root* tag that contains all the XML. The following list contains the links for all the possible
configuration options.

- [Internal configuration options](#Configuration)
    - [Path](#Path)
    
### Configuration
#### Path
**AVAILABLE ATTRIBUTES:**
- `type`
- `source`

The type attribute defines what is the internal reference and the `source` is required by the `type` attribute.
The `type` attribute can assume the following values:
- `classifier`
- `scriptModule`

If the `type` is set to `classifier` then the attribute `source` will be required and will define the path to save the
classifier's data.
If the `type` is set to `scriptModule` will set the path for the `.py` files that can be used by the chatbot answers.
[*see resource*](#Resource)

#### Resource

## Roadmap
### Big features
<table>
    <tr>
        <th>task</th>                                                       <th>status</th>
    </tr>
    <tr>
        <td>Implement wikipedia text generation using Markov Chains</td>    <td>DONE</td>
    </tr>
    <tr>
        <td>Add the sentiments module</td>                                  <td>BASICS DONE</td>
    </tr>
    <tr>
        <td>Calendar and note taking features</td>                          <td>BASICS DONE</td>
    </tr>
    <tr>
        <td>Learn systems</td>                                              <td>READY TO DEVELOP</td>
    </tr>
    <tr>
        <td>Add hacker news API to return news</td>                         <td>ON HOLD</td>
    </tr>
    <tr>
        <td>Add API capabilities</td>                                       <td>ON HOLD</td>
    </tr>
    <tr>
        <td>Build knowledge graph from user information</td>                <td>IN RESEARCH</td>
    </tr>
    <tr>
        <td>Build knowledge graph from wikipedia</td>                       <td>IN RESEARCH</td>
    </tr>
    <tr>
        <td>Add proper learning</td>                                        <td>ON HOLD</td>
    </tr>
</table>

### Maintenance tasks
<table>
    <tr>
        <th>task</th>                                                       <th>status</th>
    </tr>
    <tr>
        <td>Add C addons</td>                                               <td>IN RESEARCH - UNCERTAIN</td>
    </tr>
    <tr>
        <td>Rewrite logger</td>                                             <td>TODO</td>
    </tr>
</table>
