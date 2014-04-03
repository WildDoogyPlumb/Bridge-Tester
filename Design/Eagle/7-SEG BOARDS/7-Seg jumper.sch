<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE eagle SYSTEM "eagle.dtd">
<eagle version="6.5.0">
<drawing>
<settings>
<setting alwaysvectorfont="no"/>
<setting verticaltext="up"/>
</settings>
<grid distance="0.1" unitdist="inch" unit="inch" style="lines" multiple="1" display="no" altdistance="0.01" altunitdist="inch" altunit="inch"/>
<layers>
<layer number="1" name="Top" color="4" fill="1" visible="no" active="no"/>
<layer number="16" name="Bottom" color="1" fill="1" visible="no" active="no"/>
<layer number="17" name="Pads" color="2" fill="1" visible="no" active="no"/>
<layer number="18" name="Vias" color="2" fill="1" visible="no" active="no"/>
<layer number="19" name="Unrouted" color="6" fill="1" visible="no" active="no"/>
<layer number="20" name="Dimension" color="15" fill="1" visible="no" active="no"/>
<layer number="21" name="tPlace" color="7" fill="1" visible="no" active="no"/>
<layer number="22" name="bPlace" color="7" fill="1" visible="no" active="no"/>
<layer number="23" name="tOrigins" color="15" fill="1" visible="no" active="no"/>
<layer number="24" name="bOrigins" color="15" fill="1" visible="no" active="no"/>
<layer number="25" name="tNames" color="7" fill="1" visible="no" active="no"/>
<layer number="26" name="bNames" color="7" fill="1" visible="no" active="no"/>
<layer number="27" name="tValues" color="7" fill="1" visible="no" active="no"/>
<layer number="28" name="bValues" color="7" fill="1" visible="no" active="no"/>
<layer number="29" name="tStop" color="7" fill="3" visible="no" active="no"/>
<layer number="30" name="bStop" color="7" fill="6" visible="no" active="no"/>
<layer number="31" name="tCream" color="7" fill="4" visible="no" active="no"/>
<layer number="32" name="bCream" color="7" fill="5" visible="no" active="no"/>
<layer number="33" name="tFinish" color="6" fill="3" visible="no" active="no"/>
<layer number="34" name="bFinish" color="6" fill="6" visible="no" active="no"/>
<layer number="35" name="tGlue" color="7" fill="4" visible="no" active="no"/>
<layer number="36" name="bGlue" color="7" fill="5" visible="no" active="no"/>
<layer number="37" name="tTest" color="7" fill="1" visible="no" active="no"/>
<layer number="38" name="bTest" color="7" fill="1" visible="no" active="no"/>
<layer number="39" name="tKeepout" color="4" fill="11" visible="no" active="no"/>
<layer number="40" name="bKeepout" color="1" fill="11" visible="no" active="no"/>
<layer number="41" name="tRestrict" color="4" fill="10" visible="no" active="no"/>
<layer number="42" name="bRestrict" color="1" fill="10" visible="no" active="no"/>
<layer number="43" name="vRestrict" color="2" fill="10" visible="no" active="no"/>
<layer number="44" name="Drills" color="7" fill="1" visible="no" active="no"/>
<layer number="45" name="Holes" color="7" fill="1" visible="no" active="no"/>
<layer number="46" name="Milling" color="3" fill="1" visible="no" active="no"/>
<layer number="47" name="Measures" color="7" fill="1" visible="no" active="no"/>
<layer number="48" name="Document" color="7" fill="1" visible="no" active="no"/>
<layer number="49" name="Reference" color="7" fill="1" visible="no" active="no"/>
<layer number="51" name="tDocu" color="7" fill="1" visible="no" active="no"/>
<layer number="52" name="bDocu" color="7" fill="1" visible="no" active="no"/>
<layer number="91" name="Nets" color="2" fill="1" visible="yes" active="yes"/>
<layer number="92" name="Busses" color="1" fill="1" visible="yes" active="yes"/>
<layer number="93" name="Pins" color="2" fill="1" visible="no" active="yes"/>
<layer number="94" name="Symbols" color="4" fill="1" visible="yes" active="yes"/>
<layer number="95" name="Names" color="7" fill="1" visible="yes" active="yes"/>
<layer number="96" name="Values" color="7" fill="1" visible="yes" active="yes"/>
<layer number="97" name="Info" color="7" fill="1" visible="yes" active="yes"/>
<layer number="98" name="Guide" color="6" fill="1" visible="yes" active="yes"/>
</layers>
<schematic xreflabel="%F%N/%S.%C%R" xrefpart="/%S.%C%R">
<libraries>
<library name="Parts">
<packages>
<package name="LED_JUMPER">
<pad name="P10B" x="0" y="0" drill="1.5" shape="square"/>
<pad name="P9B" x="5.08" y="0" drill="1.5" shape="square"/>
<pad name="P8B" x="10.16" y="0" drill="1.5" shape="square"/>
<pad name="P7B" x="15.24" y="0" drill="1.5" shape="square"/>
<pad name="P6B" x="20.32" y="0" drill="1.5" shape="square"/>
<pad name="P10" x="5.08" y="-3.81" drill="0.8" shape="square"/>
<pad name="P9" x="7.62" y="-3.81" drill="0.8" shape="square"/>
<pad name="P8" x="10.16" y="-3.81" drill="0.8" shape="square"/>
<pad name="P7" x="12.7" y="-3.81" drill="0.8" shape="square"/>
<pad name="P6" x="15.24" y="-3.81" drill="0.8" shape="square"/>
<wire x1="5.08" y1="-3.81" x2="0" y2="-3.81" width="0.8128" layer="16"/>
<wire x1="0" y1="-3.81" x2="0" y2="0" width="0.8128" layer="16"/>
<wire x1="7.62" y1="-3.81" x2="7.62" y2="0" width="0.8128" layer="16"/>
<wire x1="7.62" y1="0" x2="5.08" y2="0" width="0.8128" layer="16"/>
<wire x1="10.16" y1="0" x2="10.16" y2="-3.81" width="0.8128" layer="16"/>
<wire x1="12.7" y1="-3.81" x2="12.7" y2="0" width="0.8128" layer="16"/>
<wire x1="12.7" y1="0" x2="15.24" y2="0" width="0.8128" layer="16"/>
<wire x1="15.24" y1="-3.81" x2="20.32" y2="-3.81" width="0.8128" layer="16"/>
<wire x1="20.32" y1="-3.81" x2="20.32" y2="0" width="0.8128" layer="16"/>
</package>
</packages>
<symbols>
<symbol name="LED_JUMPER">
<pin name="P10" x="-10.16" y="-5.08" length="middle" rot="R90"/>
<pin name="P9" x="-5.08" y="-5.08" length="middle" rot="R90"/>
<pin name="P8" x="0" y="-5.08" length="middle" rot="R90"/>
<pin name="P7" x="5.08" y="-5.08" length="middle" rot="R90"/>
<pin name="P6" x="10.16" y="-5.08" length="middle" rot="R90"/>
<pin name="P10B" x="-10.16" y="17.78" length="middle" rot="R270"/>
<pin name="P9B" x="-5.08" y="17.78" length="middle" rot="R270"/>
<pin name="P8B" x="0" y="17.78" length="middle" rot="R270"/>
<pin name="P7B" x="5.08" y="17.78" length="middle" rot="R270"/>
<pin name="P6B" x="10.16" y="17.78" length="middle" rot="R270"/>
<rectangle x1="-10.16" y1="0" x2="10.16" y2="12.7" layer="94"/>
</symbol>
</symbols>
<devicesets>
<deviceset name="LED_JUMPER">
<gates>
<gate name="G$1" symbol="LED_JUMPER" x="0" y="-5.08"/>
</gates>
<devices>
<device name="" package="LED_JUMPER">
<connects>
<connect gate="G$1" pin="P10" pad="P10"/>
<connect gate="G$1" pin="P10B" pad="P10B"/>
<connect gate="G$1" pin="P6" pad="P6"/>
<connect gate="G$1" pin="P6B" pad="P6B"/>
<connect gate="G$1" pin="P7" pad="P7"/>
<connect gate="G$1" pin="P7B" pad="P7B"/>
<connect gate="G$1" pin="P8" pad="P8"/>
<connect gate="G$1" pin="P8B" pad="P8B"/>
<connect gate="G$1" pin="P9" pad="P9"/>
<connect gate="G$1" pin="P9B" pad="P9B"/>
</connects>
<technologies>
<technology name=""/>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
</libraries>
<attributes>
</attributes>
<variantdefs>
</variantdefs>
<classes>
<class number="0" name="default" width="0" drill="0">
</class>
</classes>
<parts>
<part name="U$1" library="Parts" deviceset="LED_JUMPER" device=""/>
</parts>
<sheets>
<sheet>
<plain>
</plain>
<instances>
<instance part="U$1" gate="G$1" x="30.48" y="25.4"/>
</instances>
<busses>
</busses>
<nets>
</nets>
</sheet>
</sheets>
</schematic>
</drawing>
</eagle>
