Portfolioeintrag IoT Element
============================


.. important::
   Sie können erklären was ein IoT Element ist. Und machen Beispiele dazu.
   Welche haben Sie selber in der Firma oder Zuhause im Einsatz?

Was ist ein IoT Element?
------------------------

Ein IoT Element ist ein physisches Gerät, das über ein Netzwerk mit anderen Geräten oder Diensten verbunden ist.
Dabei können Daten aus der Umgebung erfasst, weitergegeben und verarbeitet werden.
Umgekehrt können über die Verbindung auch Aktionen am Gerät ausgelöst werden.

Ein IoT Element besteht dabei grundsätzlich aus verschiedenen Teilen:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Bestandteil
     - Aufgabe
   * - **Sensor**
     - Erfasst Informationen aus der realen Welt, beispielsweise Position, Temperatur oder Bewegung.
   * - **Gateway / Verarbeitung**
     - Verarbeitet beziehungsweise übermittelt die Informationen und ermöglicht die Kommunikation mit anderen Systemen.
   * - **Netzwerk**
     - Ermöglicht den Austausch der Daten mit anderen Geräten oder Diensten.
   * - **Aktor**
     - Kann eine Aktion in der realen Welt ausführen, beispielsweise einen Motor bewegen, ein Licht einschalten oder einen Ton erzeugen.

Bei einem fertigen IoT-Produkt sind diese Bestandteile meistens bereits im Gerät integriert.
Als Benutzer muss ich mich deshalb nicht darum kümmern, wie beispielsweise ein Sensor mit dem Netzwerk kommuniziert.
Ich sehe hauptsächlich die daraus entstehenden Funktionen über eine App oder einen anderen Dienst.

Vereinfacht kann man den Ablauf so darstellen:

``Umgebung → Sensor → Verarbeitung / Netzwerk → Dienst oder Aktor``

IoT Elemente bei mir Zuhause
-----------------------------

Bei mir zu Hause sind bereits verschiedene IoT Elemente im Einsatz. Besonders gut lässt sich das für mich an meinem GPS-Tracker für meinen Hund zeigen.

Tractive GPS für meinen Hund Tofu
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Mein Hund Tofu, ein Zwergspitz, trägt einen kleinen **Tractive GPS-Tracker** am Halsband.
Die offensichtlichste Funktion davon ist, dass ich über die App sehen kann, wo sich Tofu befindet.

Das Zusammenspiel zwischen dem physischen GPS-Tracker und der dazugehörigen App lässt sich auch gut an meinen eigenen Bildern erkennen:

.. list-table::
   :widths: 50 50

   * - .. figure:: ../../../_static/img/sem4/iot/iot_tractive-tofu-gps.jpeg
          :alt: Tofu mit dem Tractive GPS-Tracker am Halsband
          :align: center
          :width: 90%

          **Tractive GPS-Tracker:** Tofu mit dem kleinen GPS-Tracker am Halsband.

     - .. figure:: ../../../_static/img/sem4/iot/iot_tractive-tofu-profil.jpeg
          :alt: Screenshot des Profils von Tofu in der Tractive-App
          :align: center
          :width: 90%

          **Tractive-App:** Das Profil von Tofu in der Tractive-App, über welche die Funktionen des GPS-Trackers zur Verfügung stehen.

Die erfassten Positionsdaten werden aber für deutlich mehr verwendet als nur für einen Punkt auf einer Karte.
In der ``History`` kann ich beispielsweise sehen, wo wir unterwegs waren und welche Aktivität aufgezeichnet wurde.
Zusätzlich gibt es ein Leaderboard, über das Aktivitäten verglichen werden können.

Besonders praktisch finde ich die **Home Zone**. Ich kann einen bestimmten Bereich als Zuhause definieren.
Verlässt Tofu diesen Bereich, kann ich darüber eine Notification erhalten.

Aus einem einzelnen Messwert entsteht dadurch direkt eine zusätzliche Funktion:

``Position → Verarbeitung → Home Zone verlassen → Notification``

Der Tracker kann nicht nur Informationen liefern, sondern ich kann über die App auch Funktionen am Gerät auslösen.
Beispielsweise kann ich ein **Licht einschalten** oder einen **Ton abspielen**.
Falls ich Tofu beispielsweise im Dunkeln suchen müsste, könnte ich ihn dadurch leichter finden.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Funktion
     - Tractive GPS
   * - **Daten erfassen**
     - Position und Aktivität von Tofu werden aufgezeichnet.
   * - **Daten verarbeiten**
     - Die Position kann beispielsweise mit der definierten Home Zone verglichen werden.
   * - **Dienst**
     - Über die App erhalte ich History, Aktivitätsinformationen und Notifications.
   * - **Aktion am Gerät**
     - Licht und Ton des Trackers können über die App aktiviert werden.

Interessant finde ich ausserdem die Community-Funktion.
Andere Tractive-Nutzer können Meldungen zu Gefahren oder Auffälligkeiten in einer Umgebung erhalten.
Wenn beispielsweise irgendwo etwas für Hunde Gefährliches entdeckt wurde, kann diese Information mit anderen Nutzern geteilt werden.

Für mich ist der Tracker deshalb ein gutes Beispiel dafür, dass ein IoT Element nicht nur aus dem eigentlichen Gerät besteht.
Der GPS-Tracker ist zwar die kleine Box am Halsband, der eigentliche Nutzen entsteht aber aus dem Zusammenspiel von **Gerät, Daten, Netzwerk und App**.

.. tip::
   **Fun Fact:** Tofu hat sogar einen kleinen Einfluss auf diese Dokumentation. Das Logo meiner **HF Sphinx Documentation** ist von ihm inspiriert.

Smart-TV
~~~~~~~~

Ein weiteres IoT-Gerät bei mir zu Hause ist mein **Smart-TV**. Eine Funktion davon finde ich besonders lustig: Der Fernseher kann erkennen, wenn es in seiner Umgebung lauter wird, und seine eigene Lautstärke entsprechend anpassen.

Wenn beispielsweise jemand im Raum lauter spricht, kann dadurch auch der Fernseher lauter werden. Hier wird eine Information aus der Umgebung erfasst, verarbeitet und automatisch für eine Funktion des Geräts verwendet.

Bei einem Smart-TV sehe ich aber auch eine andere Seite von IoT. Wenn ein Gerät seine Umgebung wahrnehmen kann und gleichzeitig permanent mit dem Internet verbunden ist, stellt sich für mich die Frage, **welche Daten eigentlich erfasst werden und was anschliessend mit diesen Daten passiert**.

Vor kurzem bin ich beispielsweise auf ein YouTube-Video über LG-Fernseher gestossen. Dort wurde thematisiert, wie viele Daten moderne Smart-TVs sammeln können, wie diese weiterverarbeitet werden und dass solche Geräte teilweise auch versuchen herauszufinden, welche weiteren Geräte sich im eigenen Netzwerk befinden.

.. warning::
   **IoT bedeutet für mich deshalb auch ein zusätzliches Datenschutz- und Sicherheitsrisiko.**

   Ein Smart-TV steht direkt bei mir zu Hause und ist mit meinem Netzwerk verbunden. Als Benutzer ist für mich dabei nicht immer transparent, **welche Daten tatsächlich gesammelt werden, wohin sie übertragen werden und wofür sie anschliessend verwendet werden**.

   Dazu kommt, dass jedes zusätzliche vernetzte Gerät auch eine weitere mögliche Angriffsfläche im eigenen Netzwerk darstellt.

Das hat mir nochmals eine andere Seite von IoT gezeigt. Bei einem neuen Gerät schaut man meistens zuerst darauf, welche smarten Funktionen es bietet. Eigentlich sollte man sich aber genauso die Frage stellen, **welche Daten für diese Funktionen benötigt werden und welchen Zugriff man dem Gerät auf das eigene Netzwerk gibt**.

Weitere IoT Elemente bei mir
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ein weiteres Beispiel ist mein **Dreame-Roboterstaubsauger**, den ich bereits beim Thema IoT genauer beschrieben habe. Er kann meine Wohnung kartieren, Teppiche erkennen, selbstständig reinigen und mir Notifications senden. Über die App kann ich ihn überwachen und sogar per Remote Control direkt steuern.

Zu meinen vernetzten Geräten gehört ausserdem meine **Nespresso Vertuo Kaffeemaschine**. Die verschiedenen Beispiele zeigen mir, wie selbstverständlich IoT mittlerweile in normalen Alltagsgeräten vorhanden ist.

IoT Elemente bei meiner Arbeit
-------------------------------

Auch bei meiner Arbeit bei **Annax, a Wabtec Corporation** begegnen mir verschiedene IoT Elemente. Zwei Beispiele, mit denen ich selbst direkt zu tun habe, sind unser Badge-System und das ``HomeCenter``.

Badge-System
~~~~~~~~~~~~

Ein IoT Element, das ich bei der Arbeit praktisch jeden Tag benutze, ist unser **Badge-System**. Mit meinem Badge erhalte ich Zugang zum Gebäude und erfasse auch meine Arbeitszeit.

Das Interessante daran ist, dass der Badge beziehungsweise das Lesegerät zunächst nur eine Interaktion erfasst. Der eigentliche Nutzen entsteht durch die Weiterverarbeitung der Daten in den jeweiligen Systemen.

``Badge → Lesegerät → Identifikation → Backend-System → weitere Verarbeitung``

Beim Gebäudezugang kann beispielsweise geprüft werden, ob die entsprechende Person für einen Bereich berechtigt ist. Bei der Arbeitszeiterfassung werden die erfassten Daten wiederum in das dafür vorgesehene Tool übernommen und dort weiterverarbeitet.

.. note::
   Für mich ist daran interessant, dass **derselbe Badge unterschiedliche digitale Dienste ermöglicht**.

   Als Benutzer halte ich lediglich meinen Badge an ein Lesegerät. Im Hintergrund können die Informationen aber je nach Anwendung für den **Gebäudezugang** oder die **Arbeitszeiterfassung** verwendet und in unterschiedlichen Systemen weiterverarbeitet werden.

HomeCenter und Testanlagen
~~~~~~~~~~~~~~~~~~~~~~~~~~

Ein weiteres Beispiel aus meinem Arbeitsalltag ist unser ``HomeCenter``. Damit können wir Testanlagen verwalten sowie starten und abschalten.

Auch hier sieht man das Prinzip der Vernetzung gut: Ich muss nicht direkt am jeweiligen Gerät eine Aktion durchführen, sondern kann über ein übergeordnetes System auf die Testanlagen zugreifen und diese steuern.

Weitere vernetzte Systeme
~~~~~~~~~~~~~~~~~~~~~~~~~

Da wir Fahrgastinformationssysteme **(FIS/KIS)** für den öffentlichen Verkehr entwickeln, begegnen mir zusätzlich verschiedene vernetzte Embedded-Systeme direkt in Zügen. Dazu gehören beispielsweise **TFT-Anzeigen, Aussenanzeigen, Audio-Systeme und Systeme zur Fahrgastzählung**.

Auf diese Systeme möchte ich hier nicht im Detail eingehen. Sie zeigen für mich aber gut, dass IoT nicht nur aus Consumer-Geräten und Smart-Home-Produkten besteht, sondern auch in professionellen Embedded-Systemen eingesetzt wird.

Fazit
-----

Durch meine eigenen Beispiele wird für mich gut sichtbar, was ein IoT Element ausmacht. Das eigentliche Gerät ist nur ein Teil des Systems. Entscheidend ist vor allem, dass Informationen erfasst, über ein Netzwerk ausgetauscht und anschliessend für weitere Funktionen verwendet werden können.

Zu Hause sehe ich das besonders gut beim Tractive GPS von Tofu. Eine erfasste Position kann für die Live-Position, die ``History``, Aktivitätsinformationen und die Überwachung der ``Home Zone`` verwendet werden. Zusätzlich kann ich vom Handy aus Aktionen wie Licht oder Ton am physischen Gerät auslösen.

Bei der Arbeit finde ich besonders das Badge-System interessant, weil ich es täglich benutze, ohne gross darüber nachzudenken. Eine einfache Interaktion mit dem Badge kann im Hintergrund verschiedene Prozesse für Gebäudezugang oder Arbeitszeiterfassung auslösen.

Für mich zeigt das gut, wie breit IoT eingesetzt werden kann: **vom GPS-Tracker am Halsband über alltägliche Systeme am Arbeitsplatz bis zu Embedded-Systemen in einem Zug**.

Gleichzeitig zeigt mir das Beispiel des Smart-TVs, dass die Vernetzung nicht nur Vorteile mit sich bringt. Je mehr Geräte Daten über uns und ihre Umgebung erfassen, desto wichtiger werden auch **Datenschutz, Transparenz und IT-Sicherheit**.