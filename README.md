# Extensions for abstract argumentation
This repository is made to document the program that was used to generate admissible, complete, preferred, stable and grounded extensions for abstract argumentation, these were implemented so that they match the definition given by Dungh (1995). Furthermore the repository also includes the means of generating data about the extensions as well as the further processing of the data.

**It is not recommend to use this script for  larger graphs, as this script scales poorly.**
## Files
- The jupyter notebook file is the most user friendly file and can be used to experiment with different graphs to easily see the corresponding extensions. If the whole notebook is run then the last few cells will create the attack graphs that the user can input, as well as generating the above mentioned extensions for the attack graph.
 - The python file has the same code as the jupyter notebook, as well as a few extra functions for the collection of data of random graphs and is therefore used to create the data about the extensions suchs as the number of extensions for this graph or the length of the extensions.
 - Both of the comma-seperated values(CSV) files are the data that was generated using the python script and which were used to determine patterns for the above mentioned extension.
Finally the R file is the analysis that was performed on the data which was generated with the python script.

 ## References
 Dung, P. M. (1995). On the acceptability of arguments and its fundamental role in nonmonotonic rea-  
soning, logic programming and n-person games.  Artificial Intelligence,  77  (2), 321–357. Retrieved  
from  https://doi.org/10.1016/0004-3702(94)00041-X
