<template>

  <div id="app">

    <div class="overworld-maps">
      <l-map
        ref="map"
        :min-zoom="minZoom"
        :zoom="minZoom"
        :crs="crs"
        :center="maps[currentMap].center"
        :bounds="maps[currentMap].bounds"
        style="background-color: black;"
        @click="handleClick"
      >
        <!-- <l-image-overlay
          :url="maps['Overworld'].url"
          :bounds="maps['Overworld'].bounds"
          v-if="currentMap == 'Overworld'"
        /> -->

        <l-image-overlay v-for="(data, key) in maps" v-bind:key="key" :url="data.url" :bounds="data.bounds" v-if="currentMap == key"/>
        <l-marker
          v-for="(point, index) in points"
          :key="point.name"
          :lat-lng="point.latlng"
          :draggable="true"
          :icon="checkTypes[point.type]"
          v-on:update:latLng="updateLatLng($event, point.name, index)"
          v-if="point.map == currentMap"
        >
          <l-popup :content="'<h3>' + point.name + '</h3>'" />
        </l-marker>
        <!-- <l-polyline :lat-lngs="travel" /> -->
      </l-map>
    </div>

    <div class="pages">

    </div>

    <div class="item-pool">
      
    </div>

    <div class="dungeon-maps">
      <button 
      v-for="(data, name) in maps" 
      v-bind:key="name" 
      @click="currentMap = name" 
      v-bind:class="{buttonActive: currentMap == name}" 
      v-bind:style="{color: data.color, background: 'linear-gradient(90deg, rgba(40,40,40,1),' + data.backgroundColor + ' 100%)'}">
        <img v-bind:src="data.icon" alt=""/>
        {{name}}
      </button>
    </div>

    <div class="point-maker">
      <button @click="printData">Print</button>
      <h2>{{locations[locCount].name}}</h2>
      <button @click="nextLoc" ref="nextData">Next</button>
    </div>
  </div>
</template>

<script>
import { CRS, icon } from "leaflet";
import { LMap, LImageOverlay, LMarker, LPopup, LPolyline } from "vue2-leaflet";

import Locations from './Locations-Mine.json'
import InProgress from './in-progress.json'
// console.log(JSON.stringify(Locations))

export default {
  components: {
    LMap,
    LImageOverlay,
    LMarker,
    LPopup,
    LPolyline
  },
  methods: {
    handleClick(event) {
      console.log(this.$refs.map)
      this.lastLatLng = [event.latlng.lat, event.latlng.lng]
      this.points.push({
        name: this.locations[this.locCount].name,
        type: this.locations[this.locCount].type,
        map: this.currentMap,
        latlng: [event.latlng['lat'], event.latlng['lng']],
        // lng: event.latlng['lng'], 
        // lat: event.latlng['lat']
        })
      // console.log(this.points)
    },
    updateLatLng(event, name, index){
      // console.log(event, name)
      this.lastLatLng = [event.lat, event.lng]
      // this.points[index].latlng = [event.lat, event.lng]
    },
    nextLoc(){
      // this.locations[this.locCount].latlng = this.lastLatLng
      // this.locations.$set(this.locCount, this.lastLatLng)
      this.locationData.push({
        name: this.locations[this.locCount].name,
        type: this.locations[this.locCount].type,
        latlng: this.lastLatLng,
        map: this.currentMap,
        // lng: event.latlng['lng'], 
        // lat: event.latlng['lat']
        })
      this.locCount += 1
    },
    printData(){
      console.log(JSON.stringify(this.locationData))
      // console.log(JSON.stringify(this.points))
    }
  },
  data() {
    return {
      lastLatLng: null,
      // url: "./Maps/Overworld.png",
      // bounds: [[-26.5, -25], [1021.5, 1023]],
      bounds: [[0, 0], [1000, 1000]],
      minZoom: -3,
      crs: CRS.Simple,
      points: InProgress,
      locations: Locations,
      locCount: InProgress.length,
      locationData: [],
      currentMap: "Overworld",
      checkTypes: {
        "Chest": icon({ iconUrl: "./Icons/Chest.png", iconSize: [24, 24], iconAnchor: [12, 12]}),
        "Cutscene": icon({ iconUrl: "./Icons/Cutscene.png", iconSize: [24, 24], iconAnchor: [12, 12]}),
        "Song": icon({ iconUrl: "./Icons/Song.png", iconSize: [24, 24], iconAnchor: [12, 12]}),
        "NPC": icon({ iconUrl: "./Icons/NPC.png", iconSize: [24, 24], iconAnchor: [12, 12]}),
        "Collectable": icon({ iconUrl: "./Icons/Collectable.png", iconSize: [24, 24], iconAnchor: [12, 12]}),
        "Event": icon({ iconUrl: "./Icons/Forest.png", iconSize: [24, 24], iconAnchor: [12, 12]}),
        "Drop": icon({ iconUrl: "./Icons/Forest.png", iconSize: [24, 24], iconAnchor: [12, 12]}),
        "Boss": icon({ iconUrl: "./Icons/Forest.png", iconSize: [24, 24], iconAnchor: [12, 12]}),
        "BossHeart": icon({ iconUrl: "./Icons/BossHeart.png", iconSize: [24, 24], iconAnchor: [12, 12]}),
        "GS Token": icon({ iconUrl: "./Icons/GS Token.png", iconSize: [24, 24], iconAnchor: [12, 12]}),
        "Shop": icon({ iconUrl: "./Icons/Forest.png", iconSize: [24, 24], iconAnchor: [12, 12]}),
        "GrottoNPC": icon({ iconUrl: "./Icons/Forest.png", iconSize: [24, 24], iconAnchor: [12, 12]}),
        "GossipStone": icon({ iconUrl: "./Icons/Forest.png", iconSize: [24, 24], iconAnchor: [12, 12]}),
        
      },
      // checkTypes: {
      //   "Chest": icon({ iconUrl: "./Icons/Chest.png", iconSize: [24, 24], iconAnchor: [12, 12]}),
      //   "Cutscene": icon({ iconUrl: "./Icons/Cutscene.png", iconSize: [24, 24], iconAnchor: [12, 12]}),
      //   "Song": icon({ iconUrl: "./Icons/Song.png", iconSize: [24, 24], iconAnchor: [12, 12]}),
      //   "NPC": icon({ iconUrl: "./Icons/Forest.png", iconSize: [24, 24], iconAnchor: [12, 12]}),
      //   "Collectable": icon({ iconUrl: "./Icons/Jabu.png", iconSize: [24, 24], iconAnchor: [12, 12]}),
      //   "Event": icon({ iconUrl: "./Icons/Forest.png", iconSize: [24, 24], iconAnchor: [12, 12]}),
      //   "Drop": icon({ iconUrl: "./Icons/Forest.png", iconSize: [24, 24], iconAnchor: [12, 12]}),
      //   "Boss": icon({ iconUrl: "./Icons/Forest.png", iconSize: [24, 24], iconAnchor: [12, 12]}),
      //   "BossHeart": icon({ iconUrl: "./Icons/BossHeart.png", iconSize: [24, 24], iconAnchor: [12, 12]}),
      //   "GS Token": icon({ iconUrl: "./Icons/GS Token.png", iconSize: [24, 24], iconAnchor: [12, 12]}),
      //   "Shop": icon({ iconUrl: "./Icons/Forest.png", iconSize: [24, 24], iconAnchor: [12, 12]}),
      //   "GrottoNPC": icon({ iconUrl: "./Icons/Forest.png", iconSize: [24, 24], iconAnchor: [12, 12]}),
      //   "GossipStone": icon({ iconUrl: "./Icons/Forest.png", iconSize: [24, 24], iconAnchor: [12, 12]}),
      //   "Saria": icon({ iconUrl: "./Icons/Saria.png", iconSize: [24, 24], iconAnchor: [12, 12]}),
      //   "Zelda": icon({ iconUrl: "./Icons/Zelda.png", iconSize: [24, 24], iconAnchor: [12, 12]}),
      //   "GreatFairy": icon({ iconUrl: "./Icons/GreatFairy.png", iconSize: [24, 24], iconAnchor: [12, 12]}),
      //   "HeartPiece": icon({ iconUrl: "./Icons/HeartPiece.png", iconSize: [24, 24], iconAnchor: [12, 12]}),
        
      // },
      maps: {
        "Overworld": {url: "./Maps/Overworld.png", zoom: 0, bounds: [[0,0], [7260, 7860]], center: [3630, 3930], backgroundColor: '#FFFFFF', icon: './Icons/Overworld.png', color: "#000000"},
        "Deku Tree": {url: "./Maps/Deku.png", zoom: 0, bounds: [[0,0], [6150, 2940]], center: [3075, 1470], backgroundColor: '#00FF00', icon: './Icons/Deku.png', color: "#000000"},
        "Dodonogo's Cavern": {url: "./Maps/Dodongo.png", zoom: 0, bounds: [[0,0], [3310, 3610]], center: [1655, 1805], backgroundColor: '#FF0000', icon: './Icons/Dodongo.png', color: "#000000"},
        "Jabu Jabu": {url: "./Maps/Jabu.png", zoom: 0, bounds: [[0,0], [4790, 2830]], center: [2395, 1415], backgroundColor: '#0000FF', icon: './Icons/Jabu.png', color: "#FFFFFF"},
        "Forest Temple": {url: "./Maps/Forest.png", zoom: 0, bounds: [[0,0], [5990, 3250]], center: [2995, 1625], backgroundColor: '#00FF00', icon: './Icons/Forest.png', color: "#000000"},
        "Fire Temple": {url: "./Maps/Fire.png", zoom: 0, bounds: [[0,0], [8000, 3870]], center: [4000, 1935], backgroundColor: '#FF0000', icon: './Icons/Fire.png', color: "#000000"},
        "Water Temple": {url: "./Maps/Water.png", zoom: 0, bounds: [[0,0], [7040, 3880]], center: [3520, 1940], backgroundColor: '#0000FF', icon: './Icons/Water.png', color: "#FFFFFF"},
        "Shadow Temple": {url: "./Maps/Shadow.png", zoom: 0, bounds: [[0,0], [4370, 2990]], center: [2185, 1495], backgroundColor: '#8000FF', icon: './Icons/Shadow.png', color: "#000000"},
        "Spirit Temple": {url: "./Maps/Spirit.png", zoom: 0, bounds: [[0,0], [5060, 2730]], center: [2530, 1365], backgroundColor: '#FF8000', icon: './Icons/Spirit.png', color: "#000000"},
        "BotW": {url: "./Maps/BotW.png", zoom: 0, bounds: [[0,0], [2670, 2210]], center: [1335, 1105], backgroundColor: '#808080', icon: './Icons/BotW.png', color: "#000000"},
        "Ice Cavern": {url: "./Maps/Cavern.png", zoom: 0, bounds: [[0,0], [2470, 2500]], center: [1235, 1250], backgroundColor: '#8080FF', icon: './Icons/Cavern.png', color: "#000000"},
        "GTG": {url: "./Maps/GTG.png", zoom: 0, bounds: [[0,0], [2790, 2520]], center: [1395, 1260], backgroundColor: '#FF8000', icon: './Icons/GTG.png', color: "#000000"},
        "Ganon's Tower": {url: "./Maps/Ganon.png", zoom: 0, bounds: [[0,0], [3770, 2150]], center: [1885, 1075], backgroundColor: '#000000', icon: './Icons/Ganon.png', color: "#FFFFFF"},
        "Shops": {url: "./Maps/Ganon.png", zoom: 0, bounds: [[0,0], [3770, 2150]], center: [1885, 1075], backgroundColor: '#FFFFFF', icon: './Icons/Rupee.png', color: "#000000"},
      },
      // points: [
      //   {name: 'test', latlng: [500, 500], lat: 500, lng: 500}
      // ],
      // stars: [
      //   { name: "Sol", lng: 175.2, lat: 145.0 },
      //   { name: "Mizar", lng: 41.6, lat: 130.1 },
      //   { name: "Krueger-Z", lng: 13.4, lat: 56.5 },
      //   { name: "Deneb", lng: 218.7, lat: 8.3 }
      // ],
      travel: [[145.0, 175.2], [8.3, 218.7]]
    };
  },
  mounted() {
    this.$refs.map.mapObject.setView([3930, 3630], 1);
    window.addEventListener('keyup', (event) => {
      if (event.keyCode == 32) {
        this.$refs.nextData.click()
      }
    })
  }
};
</script>

<style>
  body {
    background-color: green;
  }

  #app {
    background-color: blue;
    position: absolute;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
  }

  .overworld-maps {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
  }

  .item-pool {
    position: absolute;
    left: 0;
    top: 0;
    background-color: red;
    width: 15vw;
    height: 100vh;
    z-index: 9999;
  }

  .item-pool button {
    position: absolute;
    right: 0;
    height: 100%;
    width: 5%;
    background-color: #00000080;
    border: none;
    font-size: 20px;
  }

  .item-pool button:hover {
    background-color: #000000A0;
  }

  .dungeon-maps {
    position: absolute;
    right: 2.5vw;
    top: 0;
    background-color: green;
    width: 0vw;
    height: 100vh;
    z-index: 9999;
    display: flex;
    flex-direction: column;
    /* overflow: hidden; */
  }

  .dungeon-maps button {
    height: 100%;
    width: 15vw;
    border: 2px solid black;
    border-radius: 45px;
    margin-top: 5px;
    margin-bottom: 5px;
    font-size: 2vmin;
    transform: translateX(0vw);
    background: linear-gradient(90deg, rgba(40,40,40,1), rgba(255,255,255,1) 100%);
    transition: all 0.5s;
    display: flex;
    justify-content: flex-start;
    align-items: center;
  }

  .dungeon-maps button img {
    position: relative;
    width: 10%;
    margin-right: 5%;
  }

  .dungeon-maps button:hover {
    /* background: linear-gradient(90deg, rgba(1,8,0,1) 0%, rgba(12,84,6,1) 41%, rgba(0,159,40,1) 100%); */
    transform: translateX(-10vw);
  }

  .dungeon-maps button:focus {
    outline: 0;
  }

  .buttonActive {
    border-color: white!important;
  }

  .point-maker {
    position: absolute;
    top: 0;
    left: 0;
    width: 500px;
    height: 100px;
    background-color: white;
    z-index: 10000;
    display: flex;
    justify-content: space-between;
  }

  .leaflet-bottom {
    display: none!important;
  }
</style>