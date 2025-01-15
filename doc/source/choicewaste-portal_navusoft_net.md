# Choice Waste

Support for schedules provided by [Choice Waste Services](https://choicewaste-portal.navusoft.net), serving central portions of the Commonwealth of Virginia, US.

## Configuration via configuration.yaml

```yaml
waste_collection_schedule:
  sources:
    - name: choicewaste-portal_navusoft_net
      args:
        username: USERNAME
        password: PASSWORD
        site_id: SITE_ID
```

### Configuration Variables

**username**
*(string) (required)*

**password**
*(string) (required)*

**site_id**
*(string) (optional)*

## Example

```yaml
waste_collection_schedule:
  sources:
    - name: choicewaste-portal_navusoft_net
      args:
        username: My User Name
        password: My Password
```

## How to get the source argument

The username and password are the same as those used to log into the customer portal at https://choicewaste-portal.navusoft.net. If the account has a single service location associated with it (as is likely the case for most residential accounts), specifying the `site_id` variable is not required. If multiple service locations are associated with the account, the first one will be selected unless the `site_id` is manually specified. The `site_id` can be identified as the eight digit number that preceeds the name and address in the `SELECT SERVICE LOCATION` dropdown list after logging into the customer portal.