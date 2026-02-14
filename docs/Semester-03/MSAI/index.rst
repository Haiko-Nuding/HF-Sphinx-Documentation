==========================
C# Programming: The Basics
==========================

C# is a modern, object-oriented, and type-safe programming language. It is designed to run on the **.NET** framework.

Structure of a C# Program
-------------------------

Every C# application follows a specific structure. At its simplest, it consists of a namespace, a class, and a `Main` method.

.. code-block:: csharp

    using System;

    namespace HelloWorldApp
    {
        class Program
        {
            static void Main(string[] args)
            {
                Console.WriteLine("Hello, World!");
            }
        }
    }

Variables and Data Types
------------------------

C# is **strongly typed**, meaning you must declare the type of a variable. Common types include:

* **int**: For integers (e.g., 100)
* **double**: For floating-point numbers (e.g., 10.99)
* **string**: For text (e.g., "Hello")
* **bool**: For Boolean values (true/false)

.. code-block:: csharp

    int age = 25;
    double price = 19.99;
    string name = "Gemini";
    bool isActive = true;

Control Flow
------------

Control flow statements allow you to add logic to your applications using loops and conditionals.

**If-Else Statement:**

.. code-block:: csharp

    if (age >= 18)
    {
        Console.WriteLine("Entry granted.");
    }
    else
    {
        Console.WriteLine("Entry denied.");
    }

**For Loop:**

.. code-block:: csharp

    for (int i = 0; i < 5; i++)
    {
        Console.WriteLine("Iteration: " + i);
    }

Classes and Objects
-------------------

C# is an **Object-Oriented Programming (OOP)** language. You define blueprints using classes and create instances called objects.

.. code-block:: csharp

    public class Car
    {
        public string Model { get; set; }
        
        public void Drive()
        {
            Console.WriteLine(Model + " is driving!");
        }
    }

    // Usage
    Car myCar = new Car();
    myCar.Model = "Tesla";
    myCar.Drive();