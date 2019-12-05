components = dict()

components["CossimOverlay"] = """"
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
