# Distributed_chat_application

Course project of Distributed Systems course by Juho Bruun and Venla Katainen


# Course project template:

# Industry track

## Project Title: Distributed peer-to-peer chat application

## About the project

## Implemented components:

Detailed description of the system architecture (Application-specific system components):
- System must have at least three nodes (e.g, containers)
- Each node must have a role: client, server, peer, broker, etc.


Participating nodes must:
- Exchange information (messages): RPC, client-server, publish/subscribe, broadcast, streaming, etc.
- Log their behavior understandably: messages, events, actions, etc.


Nodes (or their roles) do not have to be identical
For example, one acts as server, broker, monitor / admin, etc.
Each node must be an independent entity and (partially) autonomous


Detailed descriptions of relevant principles covered in the course (architecture, processes, communication, naming, synchronization, consistency and replication, fault tolerance); irrelevant principles can be left out.

### Implementation Details

Our course project is distributed peer-to-peer chat application. Using our application you can send messages using distribution. The peers can communicate directly to each other and the server is used only for the group handling.



**Architecture**:

Our application consists of one server and peers which are communication partners. The server can listen maximum of five peers so the total count of the nodes is max six. However, the application is scalable because the listening count of the server can be increased. The server is handling group joining and leaving functionality. Because the architecture is distributed peer-to-peer, peers do not need server to send or receive messages to other peers.



**Communication**:

The peers and server changes information using TCP protocol. For the communication, the IP address and port are needed to connect to the peer. We have added error handling to communication if group member (peer) or server is not available for the communication. The interaction pattern in the application is object-based.



**Naming**:

The peers needs the IP address and ports for communication. The naming scheme is attribute-based due to server's need to differentiate each peer. Also, the private message peers are identified using IPs and ports. However,the IP addresses and ports as a name of the peer can be seen also as a flat names, because those are not so human readable.



**Coordination**:

The peer handles coming messages so that the peers that connect to the peer first sends their message first and so on. The messages are shown for the users with timestamps in receiving order so the order is chronologic.



**Consistency and Replication**:

The application uses data-centric consistency model and data replication is used as well, because instead of saving the group information only in the server, also the peers have information of the group members. Also, because the server update all the group members at the same time and right away of the group changes (someone joins or leaves from the group), the replication can be seen active. Instead of using database as storage (due to already used project hours) the information of the group members is saved to text file as a json object.



**Fault Tolerance**:

We have implemented error handling for the situation where the peer or the server is not available. TCP protocol has built-in fault mitigation that simplifies our work.



**Security**:

If the application would be commercial, it absolutely should use end-to-end encrpytion in communication but unfortunately we did not have enough time to implement that.



## Built with:
Detailed description of the system functionality and how to run the implementation 

- If you are familiar with a particular container technology, feel free to use it (Docker is not mandatory)
- Any programming language can be used, such as: Python, Java, JavaScript, ..
- Any communication protocol / Internet protocol suite can be used: HTTP(S), MQTT, AMQP, CoAP, ..

### Building Details

Because the timeline and scale of the project is small, we decided not to use container technology because we are not familiar with any. The programming language of the project is Python and TCP protocol is used for communication between Python sockets used in the project.

## Getting Started:
Instructions on setting up your project locally

### HOW TO USE: Details

First, you should check that needed Python libraries are installed. 

The needed libraries are: socket, threading, sys, datetime, pickle, json, os and logging

To run application, use cmd to run client.py script. When starting the application the script asks you to input your IP address and port that can be used to connect sockets. Please note, that the script uses also port input +1 to run sockets. Also, if you want to use group message functionality and you have not joined group before, the server script is needed as well. In commercial application, the script should be run by the service provider but in our more like proof-of-concept case, some user should run the server script.

When you have started the application and input your IP address and port, you can choose if you want to join/leave group, send group message or send private message. If you select group joining/leaving, you need to input the group that you want to join/leave. The server sends the other group members back to you if the joining was successful and there was other members in the group already. Also, the other group members are informed of your joining or leaving.

When you belong to some group, you can use the name of the group to send messages to the other members. Then you should select the second option in the application. The application asks you to enter group name and message and it will send the message all the members. 

There is also a possibility to send private messages to other users. For that, you need the IP address and port of the other user. 

## Testing

Testing of the application was started with testing functionalities of the program. First, we tested how to program handles different inputs for IP address and port. We found a bug of handling those and added try/except structure and loop to check if the inputs are correct.

## Results of the tests: ------------>>>> TO BE DONE
Detailed description of the system evaluation
Evaluate your implementation using selected criteria, for example:
- Number of messages / lost messages, latencies, ...
- Request processing with different payloads, ..
- System throughput, ..


Design two evaluation scenarios that you compare with each other, for example:
- Small number / large number of messages
- Small payload / big payload

Collect numerical data of test cases:
- Collecting logs of container operations
- Conduct simple analysis for documentation purposes (e.g. plots or graphs)


## Test cases

### Test case statistics

| Passed in first try | Passed after fix | Total number of cases |
|----|----|---|
| 9 | 2 | 11 |

**Test case: Wrong input given for IP address and/or port**
- Result: Value error, socket.gaierror
- Fix: Add Try/Except structure and loop to input address and port until those can be used to bind socket
- After: Application handles wrong input correctly -> passed after fix

![Testcase_1](/images/testing_ip_port.PNG)


**Test case: Wrong input in functionality selection**
- Result: Not possible to select for example letter or wrong number -> passed in first try

![Testcase_2](/images/TC_2.PNG)

**Test case: Wrong server message**
- Result: Program stopped working if wrong server command given as a message
- Fix: Added error handling if message does not include /join or /leave
- After: Wrong input is handled correctly -> passed

![Testcase_3](/images/TC3.PNG)

**Test case: Message to group that does not exists**

- Result: Wrong group name is handled correctly -> Passed in first try

![Testcase_4](/images/TC4.PNG)

**Test case: Private message peer not available**

- Result: Cannot connect peer address/port is handled correctly -> Passed in first try

![Testcase_5](/images/TC5.PNG)

**Test case: Leave from group that does not exists**

- Result: Leaving handled correctly -> Passed in first try

![Testcase_6](/images/TC6.PNG)

**Test case: Server not available**

- Result: Handled correctly -> Passed in first try

![Testcase_7](/images/TC7.PNG)

**Test case: Send private message**

- Result: message sent successfully -> Passed in first try

![Testcase_8](/images/TC8.PNG)

**Test case: Join group**

- Result: joining successful -> Passed in first try

![Testcase_9](/images/TC9.PNG)

**Test case: Send group message**

- Result: Group message sent succesfully

![Testcase_10](/images/TC10.PNG)


**Test case: Leave from group**

- Result: Leaving from group was handled successfully

![Testcase_12](/images/TC12.PNG)

Server handles updating peers correctly as well.

![Testcase_12](/images/TC12_database.PNG)

![Testcase_12](/images/TC12_server.PNG)


## Acknowledgments:
list resources you find helpful

