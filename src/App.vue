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
          v-if="point.map == currentMap && checkVisibility[point.type]"
        >
          <l-popup :content="'<h3>' + point.name + '</h3>'" />
        </l-marker>
      </l-map>
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

    <div class="page-box" v-if="pageIsOpen">
      <button @click="pageIsOpen = false">X</button>

      <div class='main-settings' v-if="pageChoice == 'Settings'">
        <div class='setting-group' v-for="settingGroup in settings">
          <h2>{{settingGroup.text}}</h2>
          <div class='section-group' v-for="(section, index) in settingGroup.sections">
              <div class='setting-option' :class="{fullWidth: setting.type == 'SearchBox'}" v-for="setting in section.settings"  v-if="setting.text != 'Randomize Main Rule Settings'">
                <span>{{setting.text}}</span>

                <select v-model="plando['Settings'][setting.name]" v-if="setting.type == 'Combobox'">
                  <option v-for="option in setting.options" :value="option.name">
                    {{option.text}}
                  </option>
                </select>
                <input v-model="plando['Settings'][setting.name]" 
                v-else-if="setting.type == 'Checkbutton'"
                type="checkbox"
                />
                <div v-else-if="setting.type == 'Scale'">
                  <span>{{plando['Settings'][setting.name]}}</span>
                  <vue-slider v-model="plando['Settings'][setting.name]"
                  direction="ltr"
                  :min="setting.min"
                  :max="setting.max"
                  width="100px"
                  tooltip="none"
                  value='0'/>
                </div>
                <div class="search-box" v-else-if="setting.type == 'SearchBox'">
                  <div class="search-box-draggable">
                    <draggable @change="log" class="draggable" :list="settings[1]['sections'][index]['settings'][0]['options']" :group="setting.name">
                      <div v-for="location in settings[1]['sections'][index]['settings'][0]['options']" :key="location.name">
                        {{location.text}}
                      </div>
                    </draggable>
                  </div>
                  <div class="search-box-draggable">
                    <draggable @add="downloadPlando" class="draggable" :list="plando['Settings'][setting.name]" :group="setting.name">
                      <div v-for="location in plando['Settings'][setting.name]" :key="location.name">
                        {{location.text}}
                      </div>
                    </draggable>
                  </div>
                </div>
                <div v-else style="color: red;">ERROR</div>
              </div>
          </div>
        </div>
      </div>

    </div>

    <div class="pages">
      <button v-for="(data, name) in pages" @click="pageIsOpen = true; pageChoice = name">
        {{name}}
        <img v-bind:src="data.icon" alt=""/>
      </button>
    </div>

    <div class="legend" v-bind:class="{legendVis: showLegend}">
      <h2 style="align-self: center">Legend</h2>
      <div v-for="(data, key) in checkTypes">
        <button @click="checkVisibility[key] = !checkVisibility[key]">
          <img v-bind:src="'./Icons/' + key + '.png'" alt="Blah"/>
          <div v-if="checkVisibility[key]" style="position: absolute; width: 1px; height: 0px; border: 5px solid white; border-radius: 3px; top: 8px; left: 12.5px;"/>
        </button>
        <span>{{key}}</span>
      </div>
      <div class="legendButton">
        <div/>
        <button @click="showLegend = !showLegend"/>
      </div>
    </div>

    <div class="item-pool">
      
    </div>

    <!-- <div class="point-maker">
      <button @click="printData">Print</button>
      <h2>{{locations[locCount].name}}</h2>
      <button @click="nextLoc" ref="nextData">Next</button>
    </div> -->
  </div>
</template>

<script>
import { CRS, icon } from "leaflet";
import { LMap, LImageOverlay, LMarker, LPopup, LPolyline } from "vue2-leaflet";
import VueSlider from 'vue-slider-component'
import 'vue-slider-component/theme/antd.css'
import draggable from "vuedraggable"

import Locations from './Locations-Mine.json'
import InProgress from './in-progress.json'
import SettingsList from './settings_list.json'
import Plando from './Plando.json'
// console.log(JSON.stringify(Locations))

export default {
  components: {
    LMap,
    LImageOverlay,
    LMarker,
    LPopup,
    LPolyline,
    VueSlider,
    draggable
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
    },
    downloadPlando(event){
      // TODO: Make this function
      // TODO: Remember to parse through plando.Settings.allowed_tricks and plando.Settings.disabled_locations
      console.log(event)
      console.log(this)
    }
  },
  data() {
    return {
      lastLatLng: null,
      plando: Plando,
      settings: SettingsList.settingsArray.slice(1,4),
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
        // "Event": icon({ iconUrl: "./Icons/Forest.png", iconSize: [24, 24], iconAnchor: [12, 12]}),
        // "Drop": icon({ iconUrl: "./Icons/Forest.png", iconSize: [24, 24], iconAnchor: [12, 12]}),
        // "Boss": icon({ iconUrl: "./Icons/Forest.png", iconSize: [24, 24], iconAnchor: [12, 12]}),
        "BossHeart": icon({ iconUrl: "./Icons/BossHeart.png", iconSize: [24, 24], iconAnchor: [12, 12]}),
        "GS Token": icon({ iconUrl: "./Icons/GS Token.png", iconSize: [24, 24], iconAnchor: [12, 12]}),
        // "Shop": icon({ iconUrl: "./Icons/Forest.png", iconSize: [24, 24], iconAnchor: [12, 12]}),
        // "GrottoNPC": icon({ iconUrl: "./Icons/Forest.png", iconSize: [24, 24], iconAnchor: [12, 12]}),
        // "GossipStone": icon({ iconUrl: "./Icons/Forest.png", iconSize: [24, 24], iconAnchor: [12, 12]}),
        
      },
      checkVisibility: {
        "Chest": true,
        "Cutscene": true,
        "Song": true,
        "NPC": true,
        "Collectable": true,
        "BossHeart": true,
        "GS Token": true,
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
      },
      pages: {
        "Settings": {backgroundColor: '#000000', color: '#FFFFFF', icon: './Icons/Triforce.png'},
        "Item Pool": {backgroundColor: '#000000', color: '#FFFFFF', icon: './Icons/Items/FAIRY_BOW.png'},
        "Shops": {backgroundColor: '#000000', color: '#FFFFFF', icon: './Icons/Rupee.png'},
        "Boss Rewards": {backgroundColor: '#000000', color: '#FFFFFF', icon: './Icons/Old/BossHeart.png'},
        "Link": {backgroundColor: '#000000', color: '#FFFFFF', icon: './Icons/Link.png'},
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
      pageIsOpen: false,
      pageChoice: null,
      showLegend: false,
    };
  },
  mounted() {
    this.$refs.map.mapObject.setView([3630, 3930], -3);
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

  .page-box {
    position: absolute;
    top: 0;
    left: 15vw;
    width: 85vw;
    height: 100vh;
    background-color: rgba(0,0,0,0.9);
    z-index: 9998;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .page-box button {
    position: absolute;
    top: 1vw;
    left: 1vw;
    background: none;
    border: none;
    font-size: 30px;
    color: white;
  }

  /* .page-box div {
    position: relative;
    background-color: #FAFAFA;
    width: 90%;
    height: 90%;
  } */

  .main-settings {
    position: relative;
    background-color: #FAFAFA;
    width: 90%;
    height: 90%;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .setting-group {
    width: 80%;
    height: auto;
  }

  .section-group {
    width: 100%;
    height: auto;
    display: flex;
    flex-flow: wrap;
    justify-content: space-between;
  }

  .setting-option{
    width: 30%;
    min-height: 3vh;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
    margin-left: 5px;
    background-color: #D0D0D0;
  }

  .setting-option span{
    width: 50%;
    font-size: 1.5vmin;
  }

  .setting-option select{
    width: 50%;
    height: 100%;
  }

  .search-box {
    background-color: grey;
    display: flex;
  }

  .search-box-draggable {
    height: 20vh;
    width: 25vw;
    overflow-y: auto;
  }

  .draggable {
    /* background-color: purple; */
    height: 100%;
  }

  .draggable div {
    background-color: white;
    margin: 5px;
    padding: 5px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 20px;
    user-select: none;
  }

  .legendButton {
    position: absolute;
    top: 0;
    right: 0;
    width: 2vw;
    height: 100%;
    /* background-color: purple; */
  }

  .legendButton div {
    position: absolute;
    width: 2vw;
    height: 2vw;
    left: 2vw;
    width: 0; 
    height: 0; 
    border-top: 30px solid transparent;
    border-bottom: 30px solid transparent;
    border-left: 40px solid white;
  }

  .legendButton button {
    width: 2vw;
    height: 2.5vw;
    left: 2vw;
  }

  .legend {
    position: absolute;
    left: 16vw;
    top: 1vw;
    background-color: black;
    color: white;
    /* height: 100vh; */
    /* width: 10vw; */
    padding-left: 2vw;
    padding-right: 2vw;
    padding-bottom: 1vw;
    border: 5px solid white;
    border-radius: 45px;
    z-index: 9997;
    display: flex;
    flex-direction: column;
    transition: transform 0.5s;
    /* justify-content: flex-end; */
    transform: translateX(-11.5vw);
  }

  .legendVis {
    transform: translateX(0);
  }

  .legend button {
    background: none;
    border: none;
    position: relative;
  }

  .legend button:focus {
    outline: 0;
  }

  .legend div {
    display: flex;
    align-items: center;
    margin-bottom: 5px;
  }

  .legend span {
    margin-left: 5px;
  }

  .pages {
    position: absolute;
    left: 15vw;
    top: 0;
    background-color: blue;
    height: 100vh;
    width: 0vw;
    z-index: 9998;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
  }

    .pages button {
    height: 100%;
    max-height: 6vh;
    width: 15vw;
    border: 2px solid black;
    border-radius: 45px;
    margin-top: 5px;
    margin-bottom: 5px;
    font-size: 2vmin;
    transform: translateX(-12.5vw);
    background: linear-gradient(90deg, rgba(40,40,40,1), rgba(255,255,255,1) 100%);
    transition: all 0.5s;
    display: flex;
    justify-content: flex-end;
    align-items: center;
  }

  .pages button img {
    position: relative;
    width: 10%;
    margin-left: 5%;
  }

  .pages button:hover {
    /* background: linear-gradient(90deg, rgba(1,8,0,1) 0%, rgba(12,84,6,1) 41%, rgba(0,159,40,1) 100%); */
    transform: translateX(-5vw);
  }

  .pages button:focus {
    outline: 0;
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
    z-index: 9997;
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

  .fullWidth {
    width: 100%;
  }
</style>