# API Documentation - Domain Monitoring Service

The following is a **work in progress**.

> NOTE: Unless otherwise specified, all Domain Monitoring Service endpoints take their parameters as a JSON object in the request body and return a JSON object in the response.

- [API Documentation - Domain Monitoring Service](#api-documentation---domain-monitoring-service)
  - [Errors](#errors)
    - [The error object](#the-error-object)
  - [Authentication](#authentication)
  - [Groups](#groups)
    - [The group object](#the-group-object)
    - [Get all groups](#get-all-groups)
    - [Create a group](#create-a-group)
    - [Get a group](#get-a-group)
    - [Update a group](#update-a-group)
    - [Delete a group](#delete-a-group)
  - [Domains](#domains)
    - [The domain object](#the-domain-object)
    - [Get all domains](#get-all-domains)
    - [Create a domain](#create-a-domain)
    - [Get a domain](#get-a-domain)
    - [Update a domain](#update-a-domain)
    - [Delete a domain](#delete-a-domain)
  - [Domain lookalikes](#domain-lookalikes)
    - [The lookalike object](#the-lookalike-object)
    - [Get all lookalikes](#get-all-lookalikes)
    - [Get a lookalike](#get-a-lookalike)

## Errors

When an invalid request is sent, the server will send a response with the [HTTP status code](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes) in the range 400-499. The response may also contain a JSON error object in its body to provide more information.

### The error object

* `message` (string) - a brief human readable description of the error

Example:

```json
{
  "message": "Invalid file extension",
}
```

## Authentication

**TODO**

## Groups

### The group object

A record of a set of email addresses.

Attributes:

* `id` (integer) - unique identifier for the object
* `name` (string) - display name of the group
* `emails` (string) - string of email addresses seperated with semicolons
* `startAt` (string) - the date from which recurring scans should start
* `recur` (string) - how frequently the scan should recur, either `"daily"`, `"weekly"` or `"monthly"`
* `timeZone` (string) - the IANA string for the time zone to use for scheduling scans
* `createdAt` (string) - the date that the object was created
* `updatedAt` (string) - the date that the object was last updated

Example:

```json
{
  "createdAt": "2020-10-20T13:17:15.573155",
  "emails": "jbloggs@example.co.uk;jappleseed@example.com",
  "id": 1,
  "name": "Example, Inc.",
  "recur": "daily",
  "startAt": "2020-10-20T13:17:15.573155",
  "timeZone": "UTC",
  "updatedAt": "2020-10-20T13:17:15.573155"
}
```

### Get all groups

`GET /groups/`

JSON body parameters:

* `q` (string or object, optional) - search for groups that contain a string

You can supply `q` as an object to search within specific fields. For example,
supplying `"q": {"name": "foo"}` will return groups where the name
contains `"foo"`.

Returns:

* `count` (integer) - total number of group records
* `results` (array) - array of all groups

### Create a group

`POST /groups/`

JSON body parameters:

* `name` (string, required) - display name of the new group
* `emails` (string, required) - semicolon seperated list of email addresses of the new group
* `startAt` (string, optional, defaults to now) - the date from which recurring scans should start
* `recur` (string, optional, defaults to `"daily"`) - how frequently the scan should recur, either `"daily"`, `"weekly"` or `"monthly"`
* `timeZone` (string, optional, defaults to `"UTC"`) - the IANA string for the time zone to use for scheduling scans

Returns: the newly created group object

### Get a group

`GET /groups/<id>` where:

* `id` is the value of the `id` field of the group

Returns: the group object

### Update a group

Update a specific group record by setting the values of the parameters passed.
Any JSON body parameters not provided will be left unchanged.

`PUT /groups/<id>` where:

* `id` is the value of the `id` field of the group

JSON body parameters:

* `name` (string, optional) - display name of the new group
* `emails` (string, optional) - semicolon seperated list of email addresses of the group
* `startAt` (string, optional) - the date from which recurring scans should start
* `recur` (string, optional) - how frequently the scan should recur, either `"daily"`, `"weekly"` or `"monthly"`
* `timeZone` (string, optional) - the IANA string for the time zone to use for scheduling scans

Returns: the updated group object

### Delete a group

`DELETE /groups/<id>` where:

* `id` is the value of the `id` field of the group

Returns: the deleted group object

## Domains

### The domain object

Attributes:

* `id` (integer) - unique identifier for the object
* `name` (string) - DNS domain name
* `groupId` (integer) - `id` field of the group to alert for this domain
* `lastEmailed` (string or null) - date the domain's group was last sent an email regarding this domain, represented as a string
* `active` (boolean) - should this domain be scanned?
* `lastScanned` (string or null) - date when the domain was last scanned
* `numberOfScans` (integer) - number of times the domain has been scanned
* `createdAt` (string) - the date that the object was created
* `updatedAt` (string) - the date that the object was last updated

Example:

```json
{
  "active": true,
  "createdAt": "2020-10-20T13:20:45.964338",
  "groupId": 1,
  "id": 1,
  "lastEmailed": null,
  "lastScanned": null,
  "name": "www.example.com",
  "numberOfScans": 0,
  "updatedAt": "2020-10-20T13:20:45.964338"
}
```

### Get all domains

`GET /domains/`

JSON body parameters:

* `q` (string, optional) - search for domains that contain this string

Returns:

* `count` (integer) - total number of domain records
* `results` (array) - array of all domains

### Create a domain

`POST /domains/`

JSON body parameters:

* `name` (string, required) - DNS domain name for the new domain
* `groupId` (integer, required) - `id` field of the group to alert for this domain
* `active` (string, optional, defaults to `true`) - whether the domain should be scanned

Returns: the newly created domain object

### Get a domain

`GET /domains/<id>` where:

* `id` is the value of the `id` field of the domain

Returns: the domain object

### Update a domain

Update a specific domain record by setting the values of the parameters passed.
Any JSON body parameters not provided will be left unchanged.

`PUT /domains/<id>` where:

* `id` is the value of the `id` field of the domain

JSON body parameters:

* `name` (string, optional) - DNS domain name for the domain
* `groupId` (integer, optional) - `id` field of the group to alert for this domain
* `active` (string, optional) - whether the domain should be scanned

Returns: the updated domain object

### Delete a domain

`DELETE /domains/<id>` where:

* `id` is the value of the `id` field of the domain

Returns: the deleted domain object

## Domain lookalikes

### The lookalike object

A record of a site with a similar address to a monitored domain.

Attributes:

* `id` (integer) - unique identifier for the object
* `name` (string) - the DNS domain name
* `ipAddress` (string) - the IP address of the lookalike server
* `domainId` (integer) - the identifier of the domain that the lookalike is similar to
* `foundOn` (string) - the date that the lookalike was found during scanning
* `creationDate` (string) - the lookalike's creation date, as found by whois
* `updatedAt` (string) - the date the object was last updated

Example:

```json
{
  "creationDate": "2020-09-01T00:00:00",
  "domainId": 1,
  "foundOn": "2020-09-15T10:10:59.764663",
  "id": 1,
  "ipAddress": "33.33.33.33",
  "name": "www.exampl.com",
  "updatedAt": "2020-09-18T14:41:29.199971"
}
```

### Get all lookalikes

`GET /lookalikes/`

Returns:

* `count` (integer) - total number of lookalike domains
* `results` (array) - the lookalike objects

### Get a lookalike

`GET /lookalikes/<id>` where:

* `id` (integer) is the ID field of the lookalike to find

Returns: the lookalike object with the given ID