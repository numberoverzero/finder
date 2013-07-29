Finder
=========================================

Finder is a web service that aims for near parity with magiccards.info search features.

Features:

*   **Custom data hydration** Why load artist name or collector's number if you don't use them?  Specify the attributes you want filled.

*   **Paginated APIs** - Unless you like everything at once.  That's fine too.  *(Not included in initial release)*

*   **Small footprint** - All card data fits in a single ~16MB sqlite db, so you can easily download updated databases as new sets come out.

*   **Batteries included** - Want to do your own updates?  Includes scripts to add proper comparable fields to a gatherer scrape, such as cmc and integer power/toughness fields.  Full database translation in less than 15 seconds.

API
=========================================

Session Key Generation
-----------------------------------------
::

/[APIKEY]/generate?duration=[SECONDS]

Session Keys allow you to embed calls to finder in your website without exposing your account API key.
When generating session keys, you can specify a custom key duration in seconds.  The default is 300 seconds (5 minutes).


Searching
-----------------------------------------

Card queries are passed as json in the body, result settings in the querystring.

* (optional) ``fields`` is a comma-delimited list of card attributes to include in the results, such as ``fields=name,colors,cmc``.  Defaults to all fields.

* (optional) ``remove_dupes`` is a boolean to remove duplicate cards by name from results.  If true, this keeps only one instance of the newest printing of a card.  Default is true.

URI::

    /[SESSIONKEY]/search?fields=[RESULTFIELDS]&remove_dupes=true


Let's find cards that have between 4 and 6 power (inclusive), cmc of 3 or less, and are multicolored.
We only want the newest printing, and we only want name, id, and mana cost back::

    /[SESSIONKEY]/search?fields=name,id,mana&remove_dupes=true

    {
        "AND": [
            "power": ">=4",
            "power": "<=6",
            "cmc": "<=3",
            "colors": ["multi"]
        ]
    }


This can be compacted a bit, by using short names and color values::

    {
        "AND": [
            "pow": ">=4",
            "pow": "<=6",
            "cmc": "<=3",
            "c": ["m"]
        ]
    }

Note that the top-level AND is required - otherwise we would have two "pow" keys in the top-level object, which is invalid.
This is required for all queries, even if the keys are unique.

Search: Logical operators
-----------------------------------------

There are three supported logical operators: ``AND``, ``OR``, and ``NOT``.  Both ``AND`` and ``OR`` must be an array,
where each element is either a field:value pair or another logical operator.
``NOT`` is an object with a single element - any NOT object with more than one key:value pair will make the query invalid.

Finally, note that logical operators CANNOT be the value for a card field - ``"name": { "OR": ["Foo", "Bar"]}`` is invalid.

::

    {
        "AND": [
            "OR": [
                "name": "Foo",
                "name": "Bar",
            ],

            "AND": [
                "type": "Creature",
                "OR": [
                    "pow": "<5",
                    "tou": "<5"
                ]
            ],

            "NOT": {
                "set": "Return To Ravnica"
            }
        ]
    }



Search: Nesting operators
-----------------------------------------

The operators ``AND``, ``OR``, and ``NOT`` can be nested to create complex queries.
Suppose we want all creatures with cmc 3 or less, and the cards must either be blue only, or at least red and white::

    {
        "AND": [
            "cmc": "<=3",
            "type": "Creature",
            "OR": [
                "color": ["strict", "blue"],
                "color": ["red", "white", "multi"]
            ]
        ]
    }

The minimum criteria is our first two and values: it must have cmc <=3, and type "Creature".  Then, it can match one of
two criteria: either be exclusively blue, or have at least the two colors red and white.  Note that the second option
is expressed as red/white/multi, since red/white alone allows mono-red and mono-white.

Here's the compacted version::

    {
        "AND": [
            "cmc": "<=3",
            "t": "Creature",
            "OR": [
                "c": ["!", "u"],
                "c": ["r", "w", "m"]
            ]
        ]
    }

Search: Field keys and formats
-----------------------------------------

Numeric fields can use any of the following six operators::

    ==  !=  <  >  <=  >=

Strings always compare ignoring case, and non-ascii characters are replaced with their closest ascii values (mostly
removing combining characters such as accents).  The only (optional) string operator is "!" which forces a strict
match - "!Foo" will not match "FooBar" or "MyFoo".  String comparison defaults to non-strict matching
(so "foo" will match "my foo").

Examples:

* ``"artist": "John"`` would match both "John Von Bear" and "Green Johnman"

* ``"id": ">=56123"`` would match any cards with multiverse id 56123 and up.

* ``"name": "&"`` is a partial search on the name "&" which will find cards including `"Look at me, I'm R&D" <http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=74360>`_.

In the following table, type is with respect to which operators it allows.
Note that all values must be passed as strings, even numeric fields such as id or power
(because they require an operator)

+----------+----------+----------+----------+----------+----------+
|Field     |Short Name|Type      |Field     |Short Name|Type      |
+==========+==========+==========+==========+==========+==========+
|id        |id        | numeric  |flavor    |fla       | string   |
+----------+----------+----------+----------+----------+----------+
|name      |n         | string   |watermark |wat       | string   |
+----------+----------+----------+----------+----------+----------+
|type      |t         | string   |number    |num       | numeric  |
+----------+----------+----------+----------+----------+----------+
|set       |s         | string   |artist    |a         | string   |
+----------+----------+----------+----------+----------+----------+
|rarity    |r         | string   |rulings   |rul       | string   |
+----------+----------+----------+----------+----------+----------+
|power     |pow       | numeric  |cmc       |cmc       | numeric  |
+----------+----------+----------+----------+----------+----------+
|toughness |tou       | numeric  |colors    |c         | array    |
+----------+----------+----------+----------+----------+----------+
|rules     |o         | string   |loyalty   |lo        | numeric  |
+----------+----------+----------+----------+----------+----------+
|format    |f         | string   |          |          |          |
+----------+----------+----------+----------+----------+----------+

Search: Special field keys
-----------------------------------------

``colors`` is an array of strings.  Each element is either a single character, or the full name, such as "w" or "white".

* Case insensitive.

* Order isn't important.

* Duplicate values are redundant.

+----------+----------+
|Name      |Short Name|
+==========+==========+
|white     |w         |
+----------+----------+
|blue      |u         |
+----------+----------+
|black     |b         |
+----------+----------+
|red       |r         |
+----------+----------+
|green     |g         |
+----------+----------+
|multi     |m         |
+----------+----------+
|land      |l         |
+----------+----------+
|colorless |c         |
+----------+----------+
|strict    |!         |
+----------+----------+


The following returns cards that contain at least blue or at least white::

    {
        "AND": [
            "color": [
                "blue",
                "white"
            ]
        ]
    }

The following returns cards that contain blue, white, or blue and white (and no other colors)::

    {
        "AND": [
            "color": [
                "blue",
                "white",
                "strict"
            ]
        ]
    }

Finally, the following returns cards that contain both blue and white, and no other colors::

    {
        "AND": [
            "color": [
                "blue",
                "white",
                "strict",
                "multi"
            ]
        ]
    }

Search Results: As-printed fields
-----------------------------------------

Some fields such as name, power, toughness are simplified in order to make searching easier
(such as allowing ascii replacements for non-ascii characters - try search?q=name:aether for an example).
However, many users would like to access the card's printed values as well as the computed values.
Therefore these fields are available by their computed name (the same used to search) as well as the original
printed value, available as ``printed_[FIELD]``.  Currently the additional result fields are:

* ``printed_name``

* ``printed_power``

* ``printed_toughness``

* ``printed_cost`` even though there's no ``cost``.  The goal is to make it clear that the original printing of the cost is a string and can contain, for example, ``{2/g}`` as a representation for a split cost.

* ``formats`` - formats that the card is legal in
