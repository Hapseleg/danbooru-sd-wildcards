NOTE: If you only have a free then sadly this script wont be that good since you can only search for 2 tags at a time..... https://danbooru.donmai.us/upgrade

Small script for making wildcard files from danbooru for ai image generation using stable diffusion
Look here to see how that works: https://github.com/adieyal/sd-dynamic-prompts?tab=readme-ov-file


The idea is you use a pony checkpoint and want wildcard files. You use this to search for some tags, it then orders by favorite and takes the top 5 tags for that tag (there are options to filter and such).

Example:
So lets say I want more tags for a specific character, for example "son_goku":
```
input:  
        python main.py --tags son_goku
output: 
        son_goku, black_hair, breasts, 1girl, 1boy, multiple_boys,
```
breasts? 1girl?? yes, Danbooru is a lewd place, so lets filter that
```
input:  
        python main.py --username NAME --apikey KEY --tags son_goku --filtertags solo
output: 
        son_goku, 1boy, male_focus, spiked_hair, muscular, super_saiyan,
```
there we go, sfw

Long example:
```
input: 
        python main.py --username NAME --apikey KEY --tags orc,minotaur,ogre --commontags 1boy --filtertags solo,male_focus --filename monsters --limit 100 --toptagscount 10
output:
        orc, 1boy, muscular, muscular_male, colored_skin, bara, tusks, green_skin, mature_male, pectorals, facial_hair, pointy_ears,
        minotaur, 1boy, muscular, furry, horns, furry_male, bara, muscular_male, animal_ears, cow_ears, pectorals, cow_horns,
        ogre, 1boy, colored_skin, horns, bara, monster_boy, red_skin, mature_male, tusks, muscular_male, muscular, pointy_ears,
```

```
usage: main.py [-h] --tags TAGS [--commontags COMMONTAGS] [--filtertags FILTERTAGS] [--toptagscount TOPTAGSCOUNT]
               [--filename FILENAME] [--username USERNAME] [--apikey APIKEY] [--limit LIMIT]

Extract certain tags from Danbooru, for Stable diffusion wildcard files

options:
  -h, --help            show this help message and exit
  --tags TAGS           The tags, for example, 'cat,bird,dog' - csv
  --commontags COMMONTAGS
                        If you want specific common tags, such as 'no_humans,simple_background' or '1girl' etc
                        (optional) - csv
  --filtertags FILTERTAGS
                        If you want filter tags, such as 'solo' (optional) - csv
  --toptagscount TOPTAGSCOUNT
                        Specify the amount of tags you want added, defaults to 5 (optional) - number
  --filename FILENAME   If you want it to save it as a txt file in current dir (optional) - string
  --username USERNAME   The username to use with the API(optional) - string
  --apikey APIKEY       The API key for authentication (optional) - string
  --limit LIMIT         Amount of posts, defaults to 200 (optional) - int
```
