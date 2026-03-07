class Rectangle {
    var width:int
    var height:int
}

predicate can_hold(self:Rectangle, other:Rectangle)
	reads self, other
{
    self.width > other.width && self.height > other.height
}

method stretch(self:Rectangle, factor:nat) returns (rv : Rectangle)
	ensures rv.width == self.width * factor && rv.height == self.height * factor
{
    rv := new Rectangle;
    rv.width := self.width * factor;
    rv.height := self.height * factor;
    return rv;
}

method {:test} TestStretchedRectangleCanHoldOriginal() {
	var original := new Rectangle;
	original.width := 8; original.height := 7;
	var factor := 2;
	var larger := stretch(original, factor);
	assert can_hold(larger, original);
}
    
method stretched_rectangle_can_hold_original(original:Rectangle, factor:nat)
	requires original.width > 0 && original.height > 0 && factor > 1
{
	var larger := stretch(original, factor);
	assert can_hold(larger, original);
}
