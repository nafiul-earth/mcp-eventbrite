# mcp-eventbrite

1. install `uv`

3. Update the  `token` in the server configuration with your event brite API key 

```
{
  "id": "eventbrite",
  "type": "openapi",
  "endpoint": "https://www.eventbriteapi.com/v3",
  "spec_url": "",
  "spec_filepath":"eventbrite-openapi.json",
  "auth_strategy": "bearer",
  "auth": {
    "token": "xxx"
  }
}
```

2. Open a terminal in the project folder and run the command 

```
uv run main.py
```

3. To enable it for claude desktop, we would need to run it as stdio and update the code in main.py as instructed

4. update the claude desktop configuration for the mcp server  with following 

```
{
  "mcpServers": {
    "eventbrite":{
      "command":"/opt/homebrew/bin/uv", 
      "args":[
        "--directory",
        "/<Path to the folder>/mcp-eventbrite/",
        "run",
        "main.py"
      ]
    }
    
  }
}
```