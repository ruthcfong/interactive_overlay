import lucid.scratch.web.svelte as lucid_svelte


components = dict()


components["CossimOverlay"] = """
<div class="container" style="width: {size}px; height: {size}px; ">
  <div class="image" style="background-image: url({image_url}); z-index: -10; width: {size}px; height: {size}px;"></div>
  <div class="overlay" style="z-index: 10; width: {size}px; height: {size}px; left: {size/2-N/2}px; top:{size/2-N/2}px">
    <div class="overlay-inner" style="background-image: url({masks_url}); width: {N}px; height: {N}px; transform: scale({size/N}); background-position: {-pos[0]*N}px {-pos[1]*N}px; opacity: 0.7;">
    </div>
  </div>
  <div class="event-catcher" style="z-index: 20; width: {size}px; height: {size}px;" on:mousemove="set({pos: [Math.floor(N*event.offsetX/size), Math.floor(N*event.offsetY/size)]})"></div>
</div>

<div>{pos}</div>

<style>
  .container {
    position: relative;
  }
  .image, .overlay, .event-catcher {
    position: absolute;
    left: 0px;
    top: 0px;
  }
  .overlay-inner {
    image-rendering: pixelated;
  }
</style>

<script>

  export default {
    data () {
      return {
        image_url: undefined,
        size: undefined,
        N: undefined,
        masks_url: undefined,
        pos: [0,0]
      };
    },
    computed: {
    },
    helpers: {}
  };
</script>
"""


components["CossimOverlayMulti"] = """
{#each range(n_images) as n_img}
<div class="container" style="width: {size}px; height: {size}px; float: left; margin: 5px;">
  <div class="title" style="z-index: 15">{(titles == undefined) ? '' : titles[n_img]}</div>
  <div class="image" style="background-image: url({image_urls[n_img]}); z-index: -10; width: {size}px; height: {size}px;"></div>
  <div class="overlay" style="z-index: 10; width: {size}px; height: {size}px; left: {size/2-N/2}px; top:{size/2-N/2}px">
    <div class="overlay-inner" style="width: {N}px; height: {N}px; transform: scale({size/N}); background-image: url({(pos == undefined)? '' : masks_urls[pos[0]][n_img]});  background-position: {(pos == undefined)? '' : -pos[1]*N}px {(pos == undefined)? '' : -pos[2]*N}px; opacity: 0.7;">
    </div>
  </div>
  <div class="event-catcher" 
       style="z-index: 20; width: {size}px; height: {size}px;"
       on:mousemove="set({pos: [n_img, Math.floor(N*event.offsetX/size), Math.floor(N*event.offsetY/size)]})"
       on:mouseout="set({pos: undefined})"
       ></div>
</div>
{/each}

<br style="clear: both;">

<style>
  .container {
    position: relative;
  }
  .image, .overlay, .event-catcher {
    position: absolute;
    left: 0px;
    top: 0px;
  }
  .title {
    color: white;
    text-align: center;
    vertical-align: middle;
    top: 10px;
  }
  .overlay-inner {
    image-rendering: pixelated;
  }
</style>

<script>

  function range(n){
    return Array(n).fill().map((_, i) => i);
  }
  
  
  export default {
    data () {
      return {
        image_urls: undefined,
        size: undefined,
        N: undefined,
        n_images: undefined,
        masks_urls: undefined,
        pos: undefined,
        titles: undefined,
      };
    },
    computed: {
    },
    helpers: {range}
  };
</script>
"""


components["CossimOverlayMultiSeparate"] = """
{#each range(n_images) as n_img}
<div class="container" style="width: {size}px; height: {size}px; float: left; margin: 5px;">
  <div class="title" style="z-index: 15">{(titles == undefined) ? '' : titles[n_img]}</div>
  <div class="image" style="background-image: url({image_url}); z-index: -10; width: {size}px; height: {size}px;"></div>
  <div class="overlay" style="z-index: 10; width: {size}px; height: {size}px; left: {size/2-Ns[n_img]/2}px; top:{size/2-Ns[n_img]/2}px">
    <div class="overlay-inner" style="width: {Ns[n_img]}px; height: {Ns[n_img]}px; transform: scale({size/Ns[n_img]}); background-image: url({(pos == undefined)? '' : masks_urls[n_img]});  background-position: {(pos == undefined)? '' : -Ns[n_img]*Math.round(Ns[n_img]/Ns[pos[0]]*pos[1])}px {(pos == undefined)? '' : -Ns[n_img]*Math.round(Ns[n_img]/Ns[pos[0]]*pos[2])}px; opacity: 0.7;">
    </div>
  </div>
  <div class="event-catcher" 
       style="z-index: 20; width: {size}px; height: {size}px;"
       on:mousemove="set({pos: [n_img, Math.floor(Ns[n_img]*event.offsetX/size), Math.floor(Ns[n_img]*event.offsetY/size)]})"
       on:mouseout="set({pos: undefined})">
  </div>
</div>
{/each}

<br style="clear: both;">

<style>
  .container {
    position: relative;
  }
  .image, .overlay, .event-catcher {
    position: absolute;
    left: 0px;
    top: 0px;
  }
  .title {
    color: white;
    text-align: center;
    vertical-align: middle;
    top: 10px;
  }
  .overlay-inner {
    image-rendering: pixelated;
  }
</style>

<script>

  function range(n){
    return Array(n).fill().map((_, i) => i);
  }
  
  
  export default {
    data () {
      return {
        image_url: undefined,
        size: undefined,
        Ns: undefined,
        n_images: undefined,
        masks_urls: undefined,
        pos: undefined,
        titles: undefined,
      };
    },
    computed: {
    },
    helpers: {range}
  };
</script>
"""


def load_components():
    for k, v in components.items():
        lucid_svelte.html_define_svelte(k, v)
