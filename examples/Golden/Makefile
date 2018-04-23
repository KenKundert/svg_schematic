DRAWINGS = \
	charge-pump \
	inverter \
	oscillator \
	pipeline-adc \
	receiver \
	schematic

SVG_FILES=$(DRAWINGS:=.svg)
PNG_FILES=$(DRAWINGS:=.png)

.PHONY: default clean

default: $(PNG_FILES)

clean:
	@rm -rf $(PNG_FILES)

%.png: %.svg
	convert $< $@

