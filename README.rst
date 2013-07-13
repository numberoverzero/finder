Finder
=========================================

Finder is a web service that aims for parity with Gatherer search features.

Features:

*   **Familiar query format** - Uses a nearly identical syntax to `magiccards.info <magiccards.info>`_, tweaked to make room for some additional fields and search options.

*   **Custom data hydration** Why load artist name or collector's number if you don't use them?  Specify the attributes you want filled.

*   **Paginated APIs** - Unless you like everything at once.  That's fine too.  *(Available post-release)*

*   **Small footprint** - All card data fits in a single ~16MB sqlite db, so you can easily download updated databases as new sets come out.

*   **Batteries included** - Want to do your own updates?  Comes with scripts to add proper comparable fields to a gatherer scrape, such as cmc and integer power/toughness fields.  Full translation (Alpha through current) takes less than 15 seconds.

API
=========================================

Session Key Generation
-----------------------------------------
::

/[APIKEY]/generate?duration=[SECONDS]

Session Keys allow you to embed calls to finder in your website without exposing your account API key.  When generating session keys, you can specify a custom key duration in seconds.  The default is 300 seconds (5 minutes).


Searching
-----------------------------------------

When searching for cards, you don't always want all of the info available for a card.  For example, when displaying a gallery of cards with collector information (rarity, artist, set and set number) you probably don't need legal formats, converted mana cost, or rulings.  When you only need a subset of card data, use the optional ``fields`` parameter to specify which fields you want in your results.  Here's the basic format::

    /[SESSIONKEY]/search?[SEARCHTYPE]=[SEARCHSTRING]&fields=[RESULTFIELDS]&dupes=false

Currently, ``SEARCHTYPE`` is always ``q``.  This search allows the use of each field at most once, and boolean operators are not supported.  The following search is not allowed since it uses both boolean operators and specifies the name constraint twice::

    n:Birds OR (cmc<=2 AND n:Angel)

In the future, support for boolean operators (with nesting) may be added, or support for gatherer-style queries.

``SEARCHSTRING`` has a different syntax depending on which type of search you're doing.  The search string format is different for each search type - see `Search: Basic Queries`_ for more format information.

``fields`` is an optional parameter which constrains the set of card attributes that will be returned.  See `Search: Filtered Results`_ for more information.  By default, all fields are included.

``dupes`` is an optional parameter which controls whether multiple versions of the same card (by name) are returned.  By default dupes is false, and only the most recent version of a card is returned.

Search: Basic Queries
-----------------------------------------

The basic search format is::

    /[SESSIONKEY]/search?q=[SEARCHSTRING]

``SEARCHSTRING`` separates each field-op-value set (see `Search: Field keys and formats`_) with a space or plus sign::

    search?q=field1:value1+field2!"value2"+field3>=value3

Remember, values must be percent-escaped.  The following searches for cards by the artist "John" (an exact match, so "John Fields" is excluded) with converted mana cost 7 or higher and a name that includes "Something Like"::

    search?q=cmc>=7+artist!"John"+name:"Something Like"

Note that the value ``"John"`` doesn't require double quotes since there are no spaces.  Further, it's not currently possible to search for a string that includes double quotes (an escape character is not defined).

Search: Filtered Results
-----------------------------------------

The optional query parameter ``fields`` allows us to restrict the set of card attributes that are included in search results.  This is particularly valuable when searches may contain a large number of results, or we only need a small number of fields, such as name, converted mana cost, and oracle text.  In this case, a filtered search will return a much smaller amount of data.

``fields`` is a comma-separated list of fields to include for each card in the result set.  To include name, converted mana cost, and oracle text, we would use::

    /[SESSIONKEY]/search?q=[SEARCHSTRING]&fields=name,cmc,rules

All search fields and additional fields are available, so we can use ``printed_cost`` and ``cmc`` together to show cards with their actual costs, while sorting the results by cmc::

    /[SESSIONKEY]/search?q=[SEARCHSTRING]&fields=cmc,printed_cost,name

Search: Field keys and formats
-----------------------------------------

Field constraints are passed as ``[FIELD][OP][SEARCHVALUE]``.

``OP`` has different values depending on field type.  **Note**: ``[SEARCHVALUE]`` must be `percent-encoded <http://en.wikipedia.org/wiki/Percent-encoding>`_.

* Integer fields can use any of the following six operators::

    =   !   <  >  <=   >=

* String fields can use either of the following operators::

    : (partial match)  ! (exact match)

A few other notes:

* All string searches are case insensitive.

* When searching for strings with spaces, surround the entire search with double quotes: ``name!"Birds of Paradise"`` would require an exact match on the name "Birds of Paradise".

Examples:

* ``artist:John`` would match both "John Von Bear" and "Green Johnman"

* ``id>=56123`` would match any cards with multiverse id 56123 and up.

* ``name:"%26"`` is a partial search (percent-encoded) on the name "&" which will find cards including `"Look at me, I'm R&D" <http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=74360>`_.


+----------+----------+----------+----------+----------+----------+
|Field     |Short Name|Type      |Field     |Short Name|Type      |
+==========+==========+==========+==========+==========+==========+
|id        |id        | integer  |flavor    |fla       | string   |
+----------+----------+----------+----------+----------+----------+
|name      |n         | string   |watermark |wat       | string   |
+----------+----------+----------+----------+----------+----------+
|type      |t         | string   |number    |num       | integer  |
+----------+----------+----------+----------+----------+----------+
|set       |s         | string   |artist    |a         | string   |
+----------+----------+----------+----------+----------+----------+
|rarity    |r         | string   |rulings   |rul       | string   |
+----------+----------+----------+----------+----------+----------+
|power     |pow       | integer  |cmc       |cmc       | integer  |
+----------+----------+----------+----------+----------+----------+
|toughness |tou       | integer  |colors    |c         | string   |
+----------+----------+----------+----------+----------+----------+
|rules     |o         | string   |loyalty   |lo        | integer  |
+----------+----------+----------+----------+----------+----------+
|format    |f         | string   |          |          |          |
+----------+----------+----------+----------+----------+----------+

Search Results: Additional Fields
-----------------------------------------

Some fields such as name, power, toughness are simplified in order to make searching easier (such as allowing ascii replacements for non-ascii characters - try search?q=name:aether for an example).  However, many users would like to access the card's printed values as well as the computed values.  Therefore these fields are available by their computed name (the same used to search) as well as the original printed value, available as ``printed_[FIELD]``.  Currently the additional result fields are:

* ``printed_name``

* ``printed_power``

* ``printed_toughness``

* ``printed_cost`` even though there's no ``cost``.  The goal is to make it clear that the original printing of the cost is a string and can contain, for example, ``{2/g}`` as a representation for a split cost.

* ``formats`` - formats that the card is legal in
