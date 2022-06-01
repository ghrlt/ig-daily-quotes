# Instagram Quotes

Post daily quotes to your instagram account, every day.

## Installation
```bash
git clone https://github.com/ghrlt/ig-daily-quotes
```

## Usage
First of all, edit `.env` file to put your credentials. (If you don't, input will show up<br>
Then, `python3 app.py` and that's all!

## Customization
You sure can customize the posts aspects, here is how:

### Quote font
All you have to do is:
	Find a font you like, download it. Then, line 47 of `app.py` file,

```python
QUOTE_FONT = ImageFont.truetype("Raleway-SemiBold.ttf", 80)
```
replace "Raleway-SemiBold.ttf" or whatever is there by the path to your new font

*You can also change the font-size by increasing/decreasing the number, although it might need some compatibility edits in media generation*

### Author font
All you have to do is:
Find a font you like, download it. Then, line 48 of `app.py` file,

```python
AUTHOR_FONT = ImageFont.truetype("Raleway-Medium.ttf", 46)
```
replace "Raleway-Medium.ttf" or whatever is there by the path to your new font

*You can also change the font-size by increasing/decreasing the number, although it might need some compatibility edits in media generation*
	
### Colors

#### Background
Edit the color parameter with your color RGB tuple/name, line 97

```python
	img = Image.new("RGB", (1080, 1080), color=(27,27,27))
```

#### Quote
Edit the fill parameter with your color RGB tuple/name, line 116

```python
		draw.text(pos, line, fill="white", font=QUOTE_FONT)
```

#### Author
Edit the fill parameter with your color RGB tuple/name, line 118

```python
	draw.text(apos, author, fill="white", font=AUTHOR_FONT)
```

