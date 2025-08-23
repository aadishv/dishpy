_B=True
_A=None
class __generated_helper_export__:
	def __init__(A,B):A.__dict__.update(B)
def __generated_factory___init___ec0b8b3c__():return __generated_helper_export__(locals())
__generated_module___init___ec0b8b3c__=__generated_factory___init___ec0b8b3c__()
def __generated_factory_globals_7c224cbf__(__generated_import_vex_e535af88__):Brain=__generated_import_vex_e535af88__.Brain;brain=Brain();return __generated_helper_export__(locals())
__generated_module_globals_7c224cbf__=__generated_factory_globals_7c224cbf__(__generated_module___init___ec0b8b3c__)
def __generated_factory_builtintime_c9404fcf__():import time as __generated_exports_builtin_builtintime_c9404fcf__;return __generated_exports_builtin_builtintime_c9404fcf__
__generated_module_builtintime_c9404fcf__=__generated_factory_builtintime_c9404fcf__()
def __generated_factory_base_3fac3210__(__generated_import_globals_ac44b40b__,__generated_import_time_538e3ae2__):
	brain=__generated_import_globals_ac44b40b__.brain;time=__generated_import_time_538e3ae2__
	class Vec2D:
		def __init__(self,x,y):self.x=x;self.y=y
		def __add__(self,other):return Vec2D(self.x+other.x,self.y+other.y)
		def __sub__(self,other):return Vec2D(self.x-other.x,self.y-other.y)
		def __mul__(self,scalar):return Vec2D(self.x*scalar,self.y*scalar)
		def __truediv__(self,scalar):return Vec2D(self.x/scalar,self.y/scalar)
		def __str__(self):return'%s, %s'%(self.x,self.y)
	class Box:
		def __init__(self,p1,p2):self.p1=p1;self.p2=p2
		@staticmethod
		def from_topleft(x1,y1,w,h):return Box(Vec2D(x1,y1),Vec2D(x1+w,y1+h))
		def contains(self,point):return self.p1.x<=point.x<=self.p2.x and self.p1.y<=point.y<=self.p2.y
		@property
		def x1(self):return self.p1.x
		@property
		def y1(self):return self.p1.y
		@property
		def x2(self):return self.p2.x
		@property
		def y2(self):return self.p2.y
		@property
		def width(self):return self.p2.x-self.p1.x
		@property
		def height(self):return self.p2.y-self.p1.y
		def __str__(self):return'from %s to %s'%(self.p1,self.p2)
	class Component:
		def __init__(self):self.bbox=Box(Vec2D(0,0),Vec2D(0,0));self._spacing=0
		def pressed(self,pos):...
		def update_bbox(self,bbox):self.bbox=Box(p1=bbox.p1+Vec2D(self._spacing,self._spacing),p2=bbox.p2-Vec2D(self._spacing,self._spacing))
		def draw(self):...
		def spacing(self,n):self._spacing=n;return self
		def on_click(self,callback):
			def pressed(pos):self.pressed(pos);callback(pos)
			self.pressed=pressed
	def run(comp):
		brain.screen.render()
		def pressed_callback():pos=Vec2D(brain.screen.x_position(),brain.screen.y_position());comp.pressed(pos)
		brain.screen.pressed(pressed_callback);bbox=Box.from_topleft(0,0,480,232);comp.update_bbox(bbox)
		while _B:brain.screen.clear_screen();comp.draw();brain.screen.render();time.sleep(.01)
	return __generated_helper_export__(locals())
__generated_module_base_3fac3210__=__generated_factory_base_3fac3210__(__generated_module_globals_7c224cbf__,__generated_module_builtintime_c9404fcf__)
def __generated_factory_base_comps_9ae6a506__(__generated_import_base_39106495__,__generated_import_vex_45229c1c__,__generated_import_globals_3c8768e2__):
	A=False;Component=__generated_import_base_39106495__.Component;Vec2D=__generated_import_base_39106495__.Vec2D;Box=__generated_import_base_39106495__.Box;Color=__generated_import_vex_45229c1c__.Color;brain=__generated_import_globals_3c8768e2__.brain
	class Text(Component):
		def __init__(self,text,color=Color.WHITE,centered=A):super().__init__();self.text=text;self.color=color;self.centered=centered
		def pressed(self,pos):self.text='Pressed at %s, %s'%(pos.x,pos.y)
		def draw(self):
			if self.centered:x=self.bbox.x1+self.bbox.width/2-brain.screen.get_string_width(self.text)/2;y=self.bbox.y1+self.bbox.height/2
			else:x=self.bbox.x1;y=self.bbox.y1
			brain.screen.set_pen_color(self.color);brain.screen.print_at(self.text,x=x,y=y,opaque=A)
	class HStack(Component):
		def __init__(self,splits=_A,*components,adjust=_B):
			super().__init__();self.components=components
			if splits is _A:splits=[1]*len(components)
			sum_splits=sum(splits)
			if not adjust:sum_splits=1
			self.splits=[i/sum_splits for i in splits]
		def _component_at_x(self,x_pos):
			x=self.bbox.x1;i=0
			while i<len(self.components):
				width=self.bbox.width*self.splits[i]
				if x<=x_pos<x+width:return i,self.components[i],x,width
				x+=width;i+=1
			return _A,_A,_A,_A
		def pressed(self,pos):
			idx,comp,x,width=self._component_at_x(pos.x)
			if comp is not _A:comp.pressed(pos-Vec2D(x,self.bbox.y1))
		def update_bbox(self,bbox):
			super().update_bbox(bbox);x=bbox.x1;i=0
			while i<len(self.components):comp=self.components[i];width=bbox.width*self.splits[i];comp.update_bbox(Box.from_topleft(x,bbox.y1,width,bbox.height));x+=width;i+=1
		def draw(self):
			for comp in self.components:comp.draw()
	class VStack(Component):
		def __init__(self,splits=_A,*components,adjust=_B):
			super().__init__();self.components=components
			if splits is _A:splits=[1]*len(components)
			sum_splits=sum(splits)
			if not adjust:sum_splits=1
			self.splits=[i/sum_splits for i in splits]
		def _component_at_y(self,y_pos):
			y=self.bbox.y1;i=0
			while i<len(self.components):
				height=self.bbox.height*self.splits[i]
				if y<=y_pos<y+height:return i,self.components[i],y,height
				y+=height;i+=1
			return _A,_A,_A,_A
		def pressed(self,pos):
			idx,comp,y,height=self._component_at_y(pos.y)
			if comp is not _A:comp.pressed(pos)
		def update_bbox(self,bbox):
			super().update_bbox(bbox);y=bbox.y1;i=0
			while i<len(self.components):comp=self.components[i];height=bbox.height*self.splits[i];b=Box.from_topleft(bbox.x1,y,bbox.width,height);comp.update_bbox(b);y+=height;i+=1
		def draw(self):
			for comp in self.components:comp.draw()
	class Rectangle(Component):
		def __init__(self,color,radius=20,border=5):super().__init__();self.color=color;self.radius=radius;self.border_color=Color.WHITE;self.border=border
		def update_bbox(self,bbox):super().update_bbox(bbox)
		def draw(self):
			brain.screen.set_pen_color(self.color);brain.screen.draw_rectangle(self.bbox.x1+self.radius,self.bbox.y1,self.bbox.width-self.radius*2,self.bbox.height-2,self.color);brain.screen.draw_rectangle(self.bbox.x1,self.bbox.y1+self.radius,self.bbox.width-1,self.bbox.height-self.radius*2,self.color);xs=[self.bbox.x1+self.radius,self.bbox.x2-self.radius];ys=[self.bbox.y1+self.radius,self.bbox.y2-self.radius]
			for x in xs:
				for y in ys:brain.screen.draw_circle(x,y,self.radius,self.color)
			if self.border<=0:return
			brain.screen.set_pen_color(self.border_color);brain.screen.set_pen_width(self.border)
			for x in xs:
				for y in ys:
					if x==xs[0]:x_clip=self.bbox.x1
					else:x_clip=self.bbox.x2-self.radius
					if y==ys[0]:y_clip=self.bbox.y1
					else:y_clip=self.bbox.y2-self.radius
					brain.screen.set_clip_region(x_clip-2,y_clip-2,self.radius+4,self.radius+4);brain.screen.draw_circle(x,y,self.radius,Color.TRANSPARENT)
			brain.screen.set_clip_region(0,0,480,272);brain.screen.set_pen_width(self.border+2);brain.screen.draw_line(self.bbox.x1+self.radius,self.bbox.y1,self.bbox.x2-self.radius,self.bbox.y1);brain.screen.draw_line(self.bbox.x1+self.radius,self.bbox.y2,self.bbox.x2-self.radius,self.bbox.y2);brain.screen.draw_line(self.bbox.x1,self.bbox.y1+self.radius,self.bbox.x1,self.bbox.y2-self.radius);brain.screen.draw_line(self.bbox.x2,self.bbox.y1+self.radius,self.bbox.x2,self.bbox.y2-self.radius)
	class Button(Component):
		def __init__(self,text,callback):super().__init__();self.text=Text(text,centered=_B);self.rectangle=Rectangle(Color.BLUE).spacing(5);self.callback=callback
		def pressed(self,pos):print('pressed slay');self.callback(pos)
		def update_bbox(self,bbox):super().update_bbox(bbox);self.text.update_bbox(self.bbox);self.rectangle.update_bbox(self.bbox)
		def draw(self):self.rectangle.draw();self.text.draw()
	return __generated_helper_export__(locals())
__generated_module_base_comps_9ae6a506__=__generated_factory_base_comps_9ae6a506__(__generated_module_base_3fac3210__,__generated_module___init___ec0b8b3c__,__generated_module_globals_7c224cbf__)
def __generated_factory___main___0c81b9c9__(__generated_import_vex_97198221__,__generated_import_base_6cadcf38__,__generated_import_base_comps_27032ac7__,__generated_import_globals_1e76c4b5__):
	E='value';D='blue';C='red';B='name';A='color';Color=__generated_import_vex_97198221__.Color;Component=__generated_import_base_6cadcf38__.Component;Vec2D=__generated_import_base_6cadcf38__.Vec2D;run=__generated_import_base_6cadcf38__.run;HStack=__generated_import_base_comps_27032ac7__.HStack;VStack=__generated_import_base_comps_27032ac7__.VStack;Button=__generated_import_base_comps_27032ac7__.Button;brain=__generated_import_globals_1e76c4b5__.brain;autons=[{B:'Auton 1',A:C},{B:'Auton 2',A:D},{B:'Auton 3',A:C},{B:'Auton 4',A:D}];state={E:0}
	class Wrapper(Component):
		def __init__(self,i,state,autons):super().__init__();self.i=i;self.state=state;self.autons=autons
		def pressed(self,pos):self.state[E]=self.i;print('Auton ',self.autons[self.i][B],'pressed')
		def draw(self):btn=get_button(self.i,self.state,self.autons);btn.update_bbox(self.bbox);btn.draw()
	def get_button(i,state,autons):btn=Button(autons[i][B],lambda _:_A).spacing(5);btn.rectangle.color=Color.RED if autons[i][A]==C else Color.BLUE;btn.rectangle.border=5 if state[E]==i else 0;return btn
	red_indices=[i for i in range(len(autons))if autons[i][A]==C];blue_indices=[i for i in range(len(autons))if autons[i][A]==D];run(VStack([.5,.5],HStack([1]*len(red_indices),*[Wrapper(i,state,autons)for i in red_indices]),HStack([1]*len(blue_indices),*[Wrapper(i,state,autons)for i in blue_indices])))
__generated_factory___main___0c81b9c9__(__generated_module___init___ec0b8b3c__,__generated_module_base_3fac3210__,__generated_module_base_comps_9ae6a506__,__generated_module_globals_7c224cbf__)