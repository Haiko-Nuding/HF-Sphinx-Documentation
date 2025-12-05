UML Notes & Examples (Car System)
=================================

This file demonstrates **Composition** and **Aggregation** in UML, with corresponding C# code examples.

Composition Example
-------------------

**Description:**
In **composition**, the lifetime of the parts depends on the whole.
A ``Car`` **owns** an ``Engine`` and ``Wheel``'s. If the ``Car`` is destroyed, its parts are destroyed automatically.

.. uml::

   @startuml
   ' Classes
   class Car {
       - engine: Engine
       - wheels: List<Wheel>
       + Start(): void
   }

   class Engine {
       + Ignite(): void
   }

   class Wheel {
       + Rotate(): void
   }

   ' Composition relationships (filled diamond)
   Car *-- Engine
   Car *-- Wheel
   @enduml

.. code-block:: csharp

   // Car composition example
   Car car = new Car();
   car.Start(); // Uses its engine and wheels internally

   public class Car
   {
       private Engine engine;
       private List<Wheel> wheels;

       public Car()
       {
           engine = new Engine(); // created together with Car
           wheels = new List<Wheel> { new Wheel(), new Wheel(), new Wheel(), new Wheel() };
       }

       public void Start()
       {
           engine.Ignite();
           foreach (var wheel in wheels) wheel.Rotate();
       }
   }

   public class Engine
   {
       public void Ignite() { /* Engine only exists inside Car */ }
   }

   public class Wheel
   {
       public void Rotate() { /* Wheel only exists inside Car */ }
   }

Aggregation Example
-------------------

**Description:**
In **aggregation**, the parts can exist independently of the whole.
A ``Garage`` can store ``Car``'s, but ``Car``'s **exist independently** they can live before and after being in a ``Garage``.

.. uml::

   @startuml
   class Garage {
       + Park(car: Car): void
   }

   class Car {
       - engine: Engine
       - wheels: List<Wheel>
       + Start(): void
   }

   ' Aggregation relationship (open diamond)
   Garage o-- Car
   @enduml

.. code-block:: csharp

   // Cars exist independently of the Garage
   Car car1 = new Car();
   Car car2 = new Car();

   // Create a Garage and park cars
   Garage garage = new Garage();
   garage.Park(car1);
   garage.Park(car2);

   // Cars still exist even if the garage is destroyed
   garage = null;
   car1.Start();
   car2.Start();

   public class Garage
   {
       private List<Car> cars = new List<Car>();

       public void Park(Car car)
       {
           cars.Add(car);
       }
   }

   public class Car
   {
       private Engine engine;
       private List<Wheel> wheels;

       public Car()
       {
           engine = new Engine();
           wheels = new List<Wheel> { new Wheel(), new Wheel(), new Wheel(), new Wheel() };
       }

       public void Start()
       {
           engine.Ignite();
           foreach (var wheel in wheels) wheel.Rotate();
       }
   }

   public class Engine
   {
       public void Ignite() { /* Engine exists independently in Car */ }
   }

   public class Wheel
   {
       public void Rotate() { /* Wheel exists independently in Car */ }
   }
