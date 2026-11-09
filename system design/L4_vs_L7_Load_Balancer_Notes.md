# L4 vs L7 Load Balancer -- Beginner Notes

## 1. What is a load balancer?

A **load balancer** distributes incoming network traffic across multiple
backend servers.

It helps with: - **Availability:** traffic can be sent to healthy
servers. - **Scalability:** multiple servers can share the workload. -
**Performance:** helps prevent one server from becoming overloaded. -
**Fault tolerance:** health checks can detect unhealthy servers.

Typical architecture:

``` text
Clients
   |
   v
Load Balancer
   |
   +------> Application Server 1
   +------> Application Server 2
   +------> Application Server 3
                  |
                  v
               Database
```

## 2. What do L4 and L7 mean?

They refer to layers in the **OSI networking model**.

  Layer     Name          What it relates to
  --------- ------------- ----------------------------------------------
  Layer 4   Transport     TCP/UDP connections and ports
  Layer 7   Application   Application protocols and data, such as HTTP

## 3. L4 Load Balancer

A **Layer 4 load balancer** makes routing decisions using network and
transport connection information, such as source/destination IP
addresses and ports.

It does not need to inspect HTTP URLs such as `/products` or
`/payments`.

Example:

``` text
Client
  |
  | TCP connection to destination port 443
  v
L4 Load Balancer
  |
  +------> Server 1
  +------> Server 2
  +------> Server 3
```

### Common L4 characteristics

-   Operates at the transport layer.
-   Commonly handles TCP and UDP traffic.
-   Routes using IP addresses and port numbers, along with connection
    information.
-   Does not make routing decisions based on HTTP paths.
-   Often has relatively low processing overhead.
-   Suitable for applications that need TCP or UDP traffic distribution.

**Example use case:** distributing TCP connections to a group of
application servers.

## 4. L7 Load Balancer

A **Layer 7 load balancer** understands application-layer protocols such
as HTTP and HTTPS. It can inspect HTTP request information and make
routing decisions using rules.

Example:

``` text
                 Client
                   |
                   v
             L7 Load Balancer
                   |
          +--------+---------+
          |        |         |
       /products /payments  /users
          |        |         |
          v        v         v
      Product   Payment    User
      Service   Service   Service
```

### Common L7 characteristics

-   Operates at the application layer.
-   Commonly handles HTTP and HTTPS traffic.
-   Can route using URL paths, hostnames, HTTP headers, and cookies.
-   Can support features such as TLS termination, redirects, and
    application-level routing.
-   Useful for websites, APIs, and microservices.

**Example use case:** sending `/products` requests to the product
service and `/payments` requests to the payment service.

## 5. L4 vs L7: Key differences

  -----------------------------------------------------------------------
  Feature                 L4 Load Balancer        L7 Load Balancer
  ----------------------- ----------------------- -----------------------
  OSI layer               Layer 4                 Layer 7

  Layer name              Transport               Application

  Common protocols        TCP, UDP                HTTP, HTTPS

  Routing information     IP addresses, ports,    URLs, hostnames,
                          connection information  headers, cookies, and
                                                  other application data

  HTTP path routing       No                      Yes

  Application content     Does not inspect HTTP   Can inspect HTTP
  inspection              content for routing     requests

  Typical use             TCP/UDP traffic         Websites, APIs,
                          distribution            microservices

  Processing overhead     Often lower             Often higher due to
                                                  application inspection
  -----------------------------------------------------------------------

**Note:** Actual performance depends on the product, configuration,
traffic, and workload. L4 is not automatically faster in every
situation.

## 6. Practical e-commerce example

Imagine an online store at `www.shop.com` with three services:

-   Product service
-   Payment service
-   User service

### Using L4

The L4 load balancer distributes connections to backend servers based on
connection information. It does not choose a service based on the URL
path.

### Using L7

The L7 load balancer can inspect the HTTP request and route it by path:

  Request                           Destination
  --------------------------------- -----------------
  `https://www.shop.com/products`   Product service
  `https://www.shop.com/payments`   Payment service
  `https://www.shop.com/users`      User service

This is called **path-based routing**.

## 7. Examples of load-balancing products

### AWS

-   **Network Load Balancer (NLB):** primarily Layer 4; supports TCP,
    UDP, and TLS listeners.
-   **Application Load Balancer (ALB):** Layer 7; supports HTTP/HTTPS
    features such as host-based and path-based routing.

### NGINX

NGINX can be configured for: - Layer 7 reverse proxying and HTTP load
balancing. - Layer 4 TCP/UDP load balancing using its stream
functionality.

The exact capabilities depend on the NGINX edition and configuration.

## 8. Which one should you choose?

  Requirement                                Common choice
  ------------------------------------------ ---------------
  Distribute TCP connections                 L4
  Distribute UDP traffic                     L4
  Route requests by URL path                 L7
  Route requests by hostname                 L7
  HTTP/HTTPS application routing             L7
  Route API requests to different services   L7

Choose based on the protocol, routing requirements, security needs, and
performance requirements of the application.

## 9. Health checks and high availability

A load balancer can check whether backend servers are healthy.

For example:

``` text
Server 1: Healthy
Server 2: Unhealthy
Server 3: Healthy
```

The load balancer can stop sending new traffic to Server 2 while
continuing to use Servers 1 and 3.

A load balancer can itself become a **single point of failure** if
deployed as only one unprotected instance. Production architectures
should use a highly available load-balancing service or redundant
design.

## 10. Interview questions

**Q1. What is the main difference between L4 and L7 load balancing?**

L4 uses transport and connection information such as IP addresses and
ports. L7 can inspect application data such as HTTP paths, hostnames,
and headers.

**Q2. Which layer supports path-based routing?**

Layer 7.

**Q3. Which layer is commonly used to distribute TCP or UDP traffic?**

Layer 4.

**Q4. What is an AWS ALB?**

An Application Load Balancer. It operates at Layer 7 and supports
HTTP/HTTPS application routing.

**Q5. What is an AWS NLB?**

A Network Load Balancer. It primarily operates at Layer 4 and handles
connection-level traffic such as TCP and UDP.

**Q6. What is a health check?**

A periodic check used to determine whether a backend server is healthy
and able to receive traffic.

## 11. Quick memory trick

-   **L4 = IP + Port + Connection**
-   **L7 = HTTP + URL + Hostname + Headers**

Remember:

> L4 understands the network connection. L7 can understand what the
> application request is asking for.

## 12. Mini self-test

1.  You need to route `/products` and `/payments` to different services.
    Which layer is suitable?
2.  You need to distribute raw TCP connections across servers. Which
    layer is suitable?
3.  What does a health check help a load balancer identify?
4.  What can happen if a single load balancer fails and there is no
    redundancy?

### Answers

1.  L7.
2.  L4.
3.  Unhealthy or unavailable backend servers.
4.  The application may become unavailable because the load balancer is
    a single point of failure.
