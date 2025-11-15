# ReMidt Midt-Norge

Support for schedules provided by [ReMidt](https://remidt.no/) serving several municipalities in Central Norway.

## Configuration via configuration.yaml

```yaml
waste_collection_schedule:
  sources:
    - name: remidt_no
      args:
        address: Follovegen 1 A
        joined: true|false
```

### Configuration Variables

**address**  
*(string) (required)* Address for the waste collection.

**joined**  
*(boolean) (optional)* Join same-day events into one event per day.

## How to get the source arguments

Visit [remidt.no](https://remidt.no/) and make sure, address is written exactly like in the search bar.

The default is for each collection type to have separate events, so if two types are collected on the same day you will get two separate calendar events for that day. Setting the `joined` parameter to `true` will join same-day events into a single event per day instead.
