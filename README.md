Watcher
=======

Visually monitor browser usage on test machines from a single proctor machine.

Usage
=====

Server-side (test machine)
--------------------------

```
python3 tester.py {port_number} & 
```

Client-side (proctor machine)
-----------------------------

```
python3 classroom.py /path/to/classroom.xml
```

> [!NOTE]
> `classroom.py` assumes that your terminal supports colors.

Creating the XML File
=====================

The client machine, or the proctor machine takes an xml file as a command line argument.

Here is an example of an xml file with a single local machine:
```
<classroom id='local'> 
    <continent id='0'>
        <island id='0'>
            <district id='0'> 
                <address id='0' hostname='localhost' port='48999'></address>
            </district> 
        </island>
	</continent>
</classroom> 
```

The xml file serves to logically represent the physical location of the test machines 
in the classroom where the exam takes place. I thought it would be nice if the proctor
can visually see which machine is opening a browser application without having to memorize
which machines are located where in the classroom.

The Coordinate System
---------------------

From the reference point of the instructor station, or where the proctor usually stands 
during exams, I first divided the classroom into rows, which I call *continents*. I then
divide continents into columns, which I call *islands*. Islands are a desk or a cluster of 
desks where the machines are located. Continents and Islands are $y$, $x$ coordinates of 
the desks with $(0,0)$ located on the far-left corner of the classroom from the proctor's
perspective.   

Once the tables have been mapped out, I further partition the tables into *districts* and 
*addresses* to get the relative location of the machine on the table. Districts and addresses
are $y$, $x$ coordinates of the machines relative to the table they reside upon. 

The `hostname` and `port` attributes on the `address` tags will be used to make a socket 
connection. The `port` number should be the specified port number that was used to run 
`tester.py` scripts on the test machines.

Look at [`dummy.xml`](dummy.xml): <br>
<img src="img/dummy_example.png" width=500>

It is up to the user to however orient the classroom as one wishes. In the example above, 
I am assuming that the bottom of the terminal is where the instructor station is located.

> [!Note]
> Sadly, there isn't a nice graphical tool to generate the files. However, `classroom.py` can 
> be used to visualize the xml file when creating the xml file 

Server States 
=============

Disconnected
------------

When the server is not responding, or the specified port is not listening, the disconnected
state will be represented by a box with white outline and text:

<img src="img/disconnected.png" width=500>

Idle
----

When the server is connected, the color of the outline and text will turn green.

<img src="img/idle.png" width=500>

Violation
---------

When the connected server opens one of the specified browsers, the color of the outline and 
text will turn red, and the text will be flashing.

<img src="img/violation.png" width=500>
