"""
Read AI_Instruction/CreateReadMe.md in order to understand how the ReadMe.md file for each ETL project folder was generated. 

I want to have a script that loops over the sub-directories of the project, makes sure there is a go.postgresql.py file in the directory (which is the indication that it is a ETl project folde)

Then I want to append the ReadMe files to new file called ImportReadMe.md 

However, the contents of the ReadMes need to be modified in the following way: 

Replace all of the headings with a sub-heading one level deeper. So if the source Readme had a single hashtag title or line followed by equal signs.. (i.e. to the top level heading)
In the new file, this will be listed as ##
Then ## should be converted to ### and so on, so that the heading levels make sense in the merged file. 

The top-level heading should be converted to be a link into the project folder itself. 

Second, there will be relative urls linking to files within the project directory, specifically the CREATE TABLE files. 
These need to be modified so that the url resolves to the same file in the project sub-directory

"""