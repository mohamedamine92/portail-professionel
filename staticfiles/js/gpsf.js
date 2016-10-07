var map=null;
var geocoder=null;

function load()
{
	var mapdiv=document.getElementById("map_canvas");
	var mapMakerMapType=new google.maps.ImageMapType({getTileUrl:function(coord,zoom){return 'http://mt'+Math.ceil(Math.random()*3)+".google.com/vt?lyrs=mapmaker|map_type:m"+"&x="+coord.x+"&y="+coord.y+"&z="+zoom;},tileSize:new google.maps.Size(256,256),isPng:true,maxZoom:20,name:"Map Maker Normal"});
	map=new google.maps.Map(mapdiv,{zoom:15,center:new google.maps.LatLng(48.8514211,2.2920236),mapTypeId:google.maps.MapTypeId.ROADMAP});
	map.overlayMapTypes.insertAt(0,mapMakerMapType);
	geocoder=new google.maps.Geocoder();
	google.maps.event.addListener(map,"click",mapClickEvent);
	document.getElementById('address').onkeydown=keyListenAddr;
	document.getElementById('lat').onkeydown=keyListenCoord;
	document.getElementById('lon').onkeydown=keyListenCoord;
     if (document.getElementById('address').value){btnAddr2Gps() }
     else{btnGps2Addr()} 
}

function keyListenAddr(e){
	if(e==undefined)
		e=window.event;
	if(e.keyCode==13)
		btnAddr2Gps();
}

function keyListenCoord(e)
{
	if(e==undefined)
		e=window.event;
	if(e.keyCode==13)
		btnGps2Addr();
}

var marker=null;
function addrToGpsCoordinates(address)
{
	geocoder.geocode({'address':address},function(data){handleResponse(data);});
}

function handleResponse(response,pos,intent)
{
	if(marker!=null)
		marker.setMap(null);
	if(response.length==0)
	{
		alert(lang.noresult);
		return;
	}
	var address=response[0].formatted_address;
	if(pos==null)
		pos=response[0].geometry.location;
	marker=new google.maps.Marker({position:pos,map:map,title:'Address'});
	map.panTo(pos);
	var infowindow=new google.maps.InfoWindow({content:'<b>'+lang.latxlon+'</b>'+arr(pos.lat())+", "+arr(pos.lng())+'<br>'+'<b>'+lang.address+': </b>'+address+'<br>'});
	google.maps.event.addListener(marker,'click',function(){infowindow.open(map,marker);});
	document.getElementById('address').value=address;
	document.getElementById('lat').value=arr(pos.lat());
	document.getElementById('lon').value=arr(pos.lng());
	intGps2GpsDeg();
}

function gpsToAddr(lat,lng,intent)
{
	var pos=new google.maps.LatLng(lat,lng);
	geocoder.geocode({'latLng':pos},function(data){handleResponse(data,pos,intent);});
}

function btnAddr2Gps()
{
	var addr=document.getElementById('address').value;
	addrToGpsCoordinates(addr);
}

function btnGps2Addr()
{
	var lat=document.getElementById('lat').value;
	var lon=document.getElementById('lon').value;
	gpsToAddr(lat,lon);
	intGps2GpsDeg();
}

function intGps2GpsDeg()
{
	var lat=document.getElementById('lat').value;
	var lon=document.getElementById('lon').value;
	if(lat==null||isNaN(lat))
		lat=0;
	if(lon==null||isNaN(lon))
		lon=0;
	latPlus=(lat>0);
	lonPlus=(lon>0);
	document.getElementById('latOrientationN').checked=latPlus;
	document.getElementById('latOrientationS').checked=!latPlus;
	document.getElementById('lonOrientationE').checked=lonPlus;
	document.getElementById('lonOrientationW').checked=!lonPlus;
	lat=Math.abs(lat);
	lon=Math.abs(lon);
	var latDeg=Math.floor(lat);
	var latMin=Math.floor((lat-latDeg)*60);
	var latSec=(Math.round((((lat-latDeg)-(latMin/60))*60*60)*1000)/1000);
	var lonDeg=Math.floor(lon);
	var lonMin=Math.floor((lon-lonDeg)*60);
	var lonSec=(Math.round((((lon-lonDeg)-(lonMin/60))*60*60)*1000)/1000);
	document.getElementById('latDeg').value=latDeg;
	document.getElementById('latDegMinute').value=latMin;
	document.getElementById('latDegSeconde').value=latSec;
	document.getElementById('lonDeg').value=lonDeg;
	document.getElementById('lonDegMinute').value=lonMin;
	document.getElementById('lonDegSeconde').value=lonSec;
}

function btnGpsDeg2Addr()
{
	var latDeg=parseInt(document.getElementById('latDeg').value);
	if(isNaN(latDeg))
		latDeg=0;
	var latMinute=parseInt(document.getElementById('latDegMinute').value);
	if(isNaN(latMinute))
		latMinute=0;
	var latSeconde=parseInt(document.getElementById('latDegSeconde').value);
	if(isNaN(latSeconde))
		latSeconde=0;
	var lonDeg=parseInt(document.getElementById('lonDeg').value);
	if(isNaN(lonDeg))
		lonDeg=0;
	var lonMinute=parseInt(document.getElementById('lonDegMinute').value);
	if(isNaN(lonMinute))lonMinute=0;
	var lonSeconde=parseInt(document.getElementById('lonDegSeconde').value);
	if(isNaN(lonSeconde))lonSeconde=0;
	var lat=latDeg+latMinute/60+latSeconde/3600;
	var lon=lonDeg+lonMinute/60+lonSeconde/3600;
	if(document.getElementById('latOrientationS').checked)
		lat*=-1;
	if(document.getElementById('lonOrientationW').checked)
		lon*=-1;
	document.getElementById('lat').value=arr(lat);
	document.getElementById('lon').value=arr(lon);
	gpsToAddr(lat,lon);
}

function mapClickEvent(event)
{
	var pos=event.latLng;document.getElementById('lat').value=arr(pos.lat());
	document.getElementById('lon').value=arr(pos.lng());
	btnGps2Addr();
}

function arr(nb)
{
	return Math.round(nb*1000000)/1000000;
}


load();