# Economy simulator
## Story
I wanted to create a simulation that simulates how economy works. I thought that the easiest way would be to enable trading between two places: one produces grain and the other is a village with bakery. Then there are workers who travel between these places providing bread for the farmers and grain to the bakery. The proce would vary based on the demand of the village, the wealth of village, etc.

I chose python as a language for this because I'm most familiar with it. I also used pygame-module to visualize the effort of hauling stuff between villages, etc.

## Approach
I create files that are the basis of the program. There are files for settlement, workers (people actually working, not just villagers), goods (the item being delivered) and producers (places that produce goods). These are then manipulated to perform the functions.

A _settlement_ is basically any settlement that has people living in it. This can be a farming complex, a mine, a village with 20 people in it, or a mighty city with tens of bakeries, coopers, etc. These settlement have various goods that are consumed by production places and villagers.

A _worker_ is a person doing something with a resource. This (at least in the beginning of the project) can be a "hauler" that moves stuff between places, a baker, a farmer, etc. Each of these workers perform tasks in production facilities and produce goods. These goods can be consumed by villagers of used for producing something else. _Technically_ a worker is the payer and the receiver of the money from transactions between settlements, but there is no actual cash reserve on the workers

_Goods_ are resources or items that are manipulated, moved, transformed, etc. and made into new ones or consumed. Goods are stored in the settlement's warehouses or similar and are distributed from there to producers etc.

_Work orders_ are assignments that the workers take to move things around. Each workorder is considered as a set of goods that are handled. For example workorder can be "5 units of grain" or "50 units of grain". This can be divided into smaller orders if more than one worker is needed. Work order is then assigned to a worker which starts to carry the goods to the destination. Before a travel can start, the seller receives the money from the worker (technically, but not actually) and pays 10% in taxes and fees. The work order is then finalized in the buyer end by giving the money to the worker and also paying 10% in taxes and fees. The buyer receives the goods to settlement's storage.

A _producer_ is a place that creates goods from either producing gathering, hunting, mining, etc. them or refining new goods based on existing ones.

## Stage
Currently I'm trying to create a MVP for a farm to deliver grain to a town.

Utilities now contain common elements of each function that would be duplicate code for the function. This contains "file to object" and "attributes to text".

## Future plans
- Some randomness might be introduced to production rates, etc.
- A _path_ file will be crated between two settlemens which can the be used by workers. The condition can increase or decrease based on use.
- When there are crossing between delivery paths, a new town may form.
- Worker cash reserve (maybe loaning from settlements)
