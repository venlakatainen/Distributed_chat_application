# Distributed_chat_application

Course project of Distributed Systems course by Juho Bruun and Venla Katainen

## Industry track

## Project Title: Distributed peer-to-peer chat application

**Table of content:**

1. [About the Project](#about)

2. [Implementation Details](#implementation)

3. [Building Details](#building)

4. [Getting Started](#getting_started)

5. [Testing](#testing)

6. [Latency tests](#latency)

7. [Unit Tests](#unit_tests)

8. [Strss Test](#stress)

9. [Acknowledgements](#acknowledgements)

<a name="about"></a>

## 1. About the project

Chachat is the course project of Distributed Systems course by Juho Bruun and Venla Katainen

<a name="implementation"></a>

### 1.1 Implementation Details

Our course project is distributed peer-to-peer chat application. Using our application you can send messages using distribution. The peers can communicate directly to each other and the server is used only for the group handling.


**Architecture**:

Our application consists of one server and peers which are communication partners, group members. The application was tested with server and maximum 10 peers taking connection to the server. The server is handling group joining and leaving functionality. Because the architecture is distributed peer-to-peer, peers do not need server to send or receive messages to other peers. That means that peers can communicate with each other even though the server is not available.



**Communication**:

The peers and server changes information using TCP protocol using Python sockets. For the communication, the IP address and port are needed to connect to the peer. We have added error handling to communication if group member (peer) or server is not available for the communication. The interaction pattern in the application is object-based.



**Naming**:

The peers needs the IP address and ports for communication. The naming scheme is attribute-based due to server's need to differentiate each peer. Also, the private message peers are identified using IPs and ports. However,the IP addresses and ports as a name of the peer can be seen also as a flat names, because those are not so human readable. If the alias is connected to IP and Port, the naming scheme can be seen as attribute based and structured because aliases are human-readable and connected to IP and Port that are values of the alias attribute.



**Coordination**:

The peer handles coming messages so that the peers that connect to the peer first sends their message first and so on. The messages are shown for the users with timestamps in receiving order so the order is chronologic.



**Consistency and Replication**:

The application uses data-centric consistency model and data replication is used as well, because instead of saving the group information only in the server, also the peers have information of the group members in their json file. Also, because the server update all the group members at the same time and right away of the group changes (someone joins or leaves from the group), the replication can be seen active. Instead of using database as storage (due to already used project hours) the information of the group members is saved to json file. Also, when peer/user open the application, the program asks the up to the date information of the groups from the server. With this can be handled if someone leaves or joins group when the other peer is not connected or in use.



**Fault Tolerance**:

We have implemented error handling for the situation where the peer or the server is not available. TCP protocol has built-in fault mitigation that simplifies our work. Basic error handlind is implemented as well.



**Security**:

If the application would be commercial, it absolutely should use end-to-end encrpytion in communication but unfortunately we did not have enough time to implement that.



<a name="building"></a>

## 2. Building

Because the timeline and scale of the project is small, we decided not to use container technology because we are not familiar with any. The programming language of the project is Python and TCP protocol is used for communication between Python sockets used in the project.

<a name="getting_started"></a>

### 2.1 Getting Started:

Instructions on setting up your project locally.

First, you should check that needed Python libraries are installed. 

The needed libraries are: socket, threading, sys, datetime, json, os, timeit and logging

To run application, use cmd to run client.py script with command. 

```command
python client.py [port number]
```

The port in the command is used to connect sockets. Please note, that the script uses also port input +1 and -1 to run sockets. Also, if you want to use group message functionality and you have not joined group before, the server script is needed as well. In commercial application, the script should be run by the service provider but in our more like proof-of-concept case, some user should run the server script.

The server script can be run with command

```command
python server.py
```

When you have started the application and input your port, you can choose if you want to add alias, manage groups, send group message or send private message. If you select group management, you need to input the group that you want to join/leave or you can list groups. The server sends the other group members back to you if the joining was successful and there was other members in the group already. Also, the other group members are informed of your joining or leaving.

To list all commands type

```command
/help
```

To join, leave or list groups type

```command
/s
```

After that to join use command

```command
/join [group_name]
```

Leave group with command

```command
/leave [group_name]
```

and list groups that you belong with command

```command
/list
```

When you belong to some group, you can use the name of the group to send messages to the other members. To send group message use command below. group_name is the name of the group and message the message you want to send

```command
/g [group_name] [message]
```

There is also a possibility to send private messages to other users. Private message can be sent in two different ways, with IP address and port or alias. Those can be done with commands

```command
/p [ip:port] [message]
```

```command
/pa [alias] [message]
```

Finally, the alias can be added with command

```command
/a [ip:port] [alias]
```

The program can be closed with command

```command
/exit
```


<a name="testing"></a>

## 3. Testing

Testing of the application was started with testing functionalities of the program. First, we tested how to program handles different inputs for IP address and port. We found a bug of handling those and added try/except structure and loop to check if the inputs are correct. Also, we tested different inputs for selection, peer connection, group joining and leaving. Many functionalities were working correctly right away, but some issues needed to be fixed and tested again. 

<a name="latency"></a>

### 3.1 Latency tests

We tested latency using Python timeit module. Both group joining and leaving latencies were good.

Function | Group joining | Group leaving |
|---|---|---|
Information change with server | 0.0030354000627994537 | 0.002914200071245432 |
Information change with server + database handling in peer side | 0.005914099980145693 | 0.004863199777901173 |

As can be seen from the results, in both cases the group leaving was a little bit faster than group joining. However, neither of them can be said to slow down the program.

**Group joining latency (message sending and receiving with server)**

- Result: 0.0030354000627994537

![Testcase_13](/images/TC13.PNG)

Latency stayed also stabile eventhough two peers were joining to the group at the same time

![Testcase_14](/images/TC14.PNG)

**Group leaving latency (message sending and receiving with server)**

- Result: 0.002914200071245432

![Testcase_15](/images/TC15.PNG)

**Latency of group joining and handling database in peer side**

- Result: 0.005914099980145693

![Testcase_16](/images/TC16.PNG)

**Latency of group leaving and handling database in peer side**

- Result: 0.004863199777901173

![Testcase_17](/images/TC17.PNG)

<a name="unit_tests"></a>

### 3.2 Unit Test cases

### Test case statistics

| Passed in first try | Passed after fix | Total number of cases |
|----|----|---|
| 12 | 2 | 14 |

**Test case: Wrong input given for IP address and/or port**
- Result: Value error, socket.gaierror
- Fix: Add Try/Except structure and loop to input address and port until those can be used to bind socket
- After: Application handles wrong input correctly -> passed after fix

![Testcase_1](/images/testing_ip_port.PNG)


**Test case: Wrong input in functionality selection (functionality improved later)**
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

**Test case: invalid server command after UI implementation**

- Result: handled correctly -> passed with the first try

![Testcase_18](/images/TC18.PNG)

**Test case: Successfull group joining and leaving after UI implementation**

-Result: Passed in first try

![Testcase_19](/images/TC19.PNG)

**Test case: group leaving with error handled succesfully**

- Result: Passed in first try

![Testcase_20](/images/TC20.PNG)


<a name="stress"></a>

### 3.3 Stress test

We tested how much peers the group handling server can handle. The server worked correctly even with ten connected peers. The test was done manually so with more peers, the test was not tried. 

![Testcase_17](/images/TC17.PNG)

<a name="acknowledgements"></a>

## 4. Acknowledgments:

Mostly used Python modules' documentation 

