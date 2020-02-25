<template>

  <div id="app">

    <div class="overworld-maps">
      <l-map
        ref="map"
        :min-zoom="minZoom"
        :zoom="maps[currentMap].zoom"
        :crs="crs"
        :center="[500, 500]"
        :maxBounds="[100, 100]"
        style="background-color: black;"
        @click="handleClick"
      >
        <l-image-overlay
          :url="maps[currentMap].url"
          :bounds="bounds"
        />
        <l-marker
          v-for="point in points"
          :key="point.name"
          :lat-lng="point.latlng"
          :draggable="true"
          v-on:update:latLng="updateLatLng($event, point.name)"
        >
          <!-- <l-popup :content="point.name" /> -->
        </l-marker>
        <!-- <l-polyline :lat-lngs="travel" /> -->
      </l-map>
    </div>

    <div class="item-pool">
      <button>
        <
      </button>
    </div>

    <div class="dungeon-maps">
      <button v-for="(data, name) in maps" v-bind:key="name" @click="currentMap = name">{{name}}</button>
    </div>

    <div class="point-maker">
      <button @click="printData">Print</button>
      <h2>{{locations[locCount].name}}</h2>
      <button @click="nextLoc" ref="nextData">Next</button>
    </div>
  </div>
</template>

<script>
import { CRS } from "leaflet";
import { LMap, LImageOverlay, LMarker, LPopup, LPolyline } from "vue2-leaflet";

import Locations from './Locations-Mine.json'
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
      // console.log(event.latlng)
      this.lastLatLng = [event.latlng.lat, event.latlng.lng]
      this.points.push({
        name: this.locations[this.locCount].name,
        type: this.locations[this.locCount].type,
        latlng: [event.latlng['lat'], event.latlng['lng']],
        // lng: event.latlng['lng'], 
        // lat: event.latlng['lat']
        })
      // console.log(this.points)
    },
    updateLatLng(event, name){
      // console.log(event, name)
      this.lastLatLng = [event.lat, event.lng]
    },
    nextLoc(){
      // this.locations[this.locCount].latlng = this.lastLatLng
      // this.locations.$set(this.locCount, this.lastLatLng)
      this.locationData.push({
        name: this.locations[this.locCount].name,
        type: this.locations[this.locCount].type,
        latlng: this.lastLatLng,
        // lng: event.latlng['lng'], 
        // lat: event.latlng['lat']
        })
      this.locCount += 1
    },
    printData(){
      console.log(JSON.stringify(this.locationData))
    }
  },
  data() {
    return {
      lastLatLng: null,
      // url: "./Maps/Overworld.png",
      bounds: [[-26.5, -25], [1021.5, 1023]],
      minZoom: -3,
      crs: CRS.Simple,
      points: [{"name":"Kokiri Sword Chest","type":"Chest","latlng":[37.75,581]},{"name":"Mido Chest Top Left","type":"Chest","latlng":[89.8125,577]},{"name":"Mido Chest Top Right","type":"Chest","latlng":[90.125,580.0625]},{"name":"Mido Chest Bottom Left","type":"Chest","latlng":[86.75,577.125]},{"name":"Mido Chest Bottom Right","type":"Chest","latlng":[86.8125,579.8125]}],
      locations: Locations,
      locCount: 0,
      locationData: [],
      currentMap: "Overworld",
      maps: {
        "Overworld": {url: "./Maps/Overworld.png", zoom: 0, center: [500, 500]},
        "Deku Tree": {url: "./Maps/Deku.png", zoom: -1, center: [500, 500]},
        "Dodonogo's Cavern": {url: "./Maps/Dodongo.png", zoom: 0, center: [500, 500]},
        "Jabu Jabu": {url: "./Maps/Jabu.png", zoom: 0, center: [500, 500]},
        "Forest Temple": {url: "./Maps/Forest.png", zoom: 0, center: [500, 500]},
        "Fire Temple": {url: "./Maps/Fire.png", zoom: -1, center: [500, 500]},
        "Water Temple": {url: "./Maps/Water.png", zoom: -1, center: [500, 500]},
        "Shadow Temple": {url: "./Maps/Shadow.png", zoom: -1, center: [500, 500]},
        "Spirit Temple": {url: "./Maps/Spirit.png", zoom: -1, center: [500, 500]},
        "BotW": {url: "./Maps/BotW.png", zoom: 0, center: [500, 500]},
        "Ice Cavern": {url: "./Maps/Cavern.png", zoom: 0, center: [500, 500]},
        "Ganon's Tower": {url: "./Maps/Ganon.png", zoom: 0, center: [500, 500]},
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
    this.$refs.map.mapObject.setView([500, 500], 1);
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
    right: 0;
    top: 0;
    background-color: green;
    width: 15vw;
    height: 100vh;
    z-index: 9999;
    display: flex;
    flex-direction: column;
  }

  .dungeon-maps button {
    height: 100%;
    width: 100%;
    border: 2px solid black;
    background: linear-gradient(90deg, rgba(6,36,0,1) 0%, rgba(17,121,9,1) 41%, rgba(0,255,64,1) 100%);
  }

  .dungeon-maps button:hover {
    background: linear-gradient(90deg, rgba(1,8,0,1) 0%, rgba(12,84,6,1) 41%, rgba(0,159,40,1) 100%);
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

  .leaflet-container img {
max-width: none !important;
}
</style>