# Economy simulator
## Story
I wanted to create a simulation that simulates how economy works. I thought that the easiest way would be to enable trading between two places: one produces grain and the other is a village with bakery. Then there are workers who travel between these places providing bread for the farmers and grain to the bakery. The proce would vary based on the demand of the village, the wealth of village, etc.

I chose python as a language for this because I'm most familiar with it. I also used pygame-module to visualize the effort of hauling stuff between villages, etc.

## Approach
| I create files that are the basis of the program. There are files for settlement, workers (people actually working, not just villagers), goods (the item being delivered) and producers (places that produce goods). These are then manipulated to perform the functions.

I changed my approach just using objects instead of file system. Even thought testability was in mind with the files, that can be circumvented by havin a configuration file instead. Configuration file now consists of lines representing an item (settlement, worker, etc.) and these lines are then converted into objects. In the future maybe there will be a json, yaml, or similar config file, but a text file will do for now.

A _settlement_ is basically any settlement that has people living in it. This can be a farming complex, a mine, a village with 20 people in it, or a mighty city with tens of bakeries, coopers, etc. These settlement have various goods that are consumed by production places and villagers. Some settlements irregularly require some luxury items (jewlwery, meat, clothes, etc.) that are only requiested for a brief time. Most usual settlements are the following:
- Farming settlement with 5 inhabitants (produces _grain_)
- Hamlet with 20 inhabitants (produces _bread from grain_ which is then divided to citizens so that all inhabitants are fed and the rest is sold.)
- ...

A _worker_ is a person doing something with a resource. This (at least in the beginning of the project) can be a "hauler" that moves stuff between places, a baker, a farmer, etc. Each of these workers perform tasks in production facilities and produce goods. These goods can be consumed by villagers of used for producing something else. _Technically_ a worker is the payer and the receiver of the money from transactions between settlements, but there is no actual cash reserve on the workers

_Goods_ are resources or items that are manipulated, moved, transformed, etc. and made into new ones or consumed. Goods are stored in the settlement's warehouses or similar and are distributed from there to producers etc.

_Work orders_ are assignments that the workers take to move things around. Each workorder is considered as a set of goods that are handled. For example workorder can be "5 units of grain" or "50 units of grain". This can be divided into smaller orders if more than one worker is needed. Work order is then assigned to a worker which starts to carry the goods to the destination. Before a travel can start, the seller receives the money from the worker (technically, but not actually) and pays 10% in taxes and fees. The work order is then finalized in the buyer end by giving the money to the worker and also paying 10% in taxes and fees. The buyer receives the goods to settlement's storage.

A _producer_ is a place that creates goods from either producing gathering, hunting, mining, etc. them or refining new goods based on existing ones.

## Stage
A worker can now be attached to a work order and deliver it to the correct place. This has been a Proof of concept and found to be working. The code is quite complex and with testing it can be eventually refactored.

Running the script can now perform a calculation where it attaches workers to work assignments, etc. The work is still to be done on how to finish the delivery process. Also, extensive testing needs to be done since a lot has been developed "in rush to get an MVP done". Now that there is somewhat functioning MVP, testing can really commence.

## Future plans
- Some randomness might be introduced to production rates, etc.
- A _path_ file will be crated between two settlemens which can the be used by workers. The condition can increase or decrease based on use.
- When there are crossing between delivery paths, a new town may form.
- Worker cash reserve (maybe loaning from settlements)
- New settlements created using a template (farm, etc.)

## Testing
Testing is done using *unittest*. Tests on workers, work orders, settlements, and producers will contain tests that focus on creation of objects. Unittest "patch" is used to insert test data to the function under test. The tests are documented so that the scoped out elements are documented.