import webbrowser
import os
import re

# Styles and scripting for the page
main_page_head = '''
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Movie Trailers</title>
    <!-- Styling -->
    <link rel="stylesheet" type="text/css" href="css/bootstrap.min.css">
    <link rel="stylesheet" type="text/css" href="css/style.css">
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
    <link href="https://fonts.googleapis.com/css?family=Bungee+Inline" rel="stylesheet">
    <!-- JavaScript for modal -->
    <script type="text/javascript">
      // Pause the video when the modal is closed
      $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
          // Remove the src so the player itself gets removed, as this is the only
          // reliable way to ensure the video stops playing in IE
          $("#trailer-video-container").empty();
      });
      // Start playing the video whenever the trailer modal is opened
      $(document).on('click', '.movie-tile', function (event) {
          var trailerYouTubeId = $(this).attr('data-trailer-youtube-id')
          var sourceUrl = 'http://www.youtube.com/embed/' + trailerYouTubeId + '?autoplay=1&html5=1';
          $("#trailer-video-container").empty().append($("<iframe></iframe>", {
            'id': 'trailer-video',
            'type': 'text-html',
            'src': sourceUrl,
            'frameborder': 0
          }));
      });
      // Animate in the movies when the page loads
      $(document).ready(function () {
        $('.movie-tile').hide().first().show("fast", function showNext() {
          $(this).next("div").show("fast", showNext);
        });
      });
    </script>
  </head>
'''

# The main page layout and title bar
main_page_content = '''
<body>
  <!-- Trailer Video Modal -->
  <div class="modal" id="trailer">
    <div class="modal-dialog">
      <div class="modal-content">
        <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
        <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24" alt="exit window cross"/>
        </a>
        <div class="scale-media" id="trailer-video-container">
        </div>
      </div>
    </div>
  </div>
  <!-- Main Page Content -->
  <!--Top Bar-->
  <div class="row">
    <nav class="navbar navbar-inverse">
      <div class="col-md-6">
        <h1 class="title-text">Fresh Tomatoes!</h1>
      </div>
      <div class="col-md-6">
        <div id="rightmenu">
          <ul>
            <li><a href="#">Sign Up</a></li>
            <li><a href="#">Login</a></li>
          </ul>
        </div>
      </div>
    </nav>
  </div>
  <!--Intro-->
  <div class="row trailerrow">
    <iframe width="100%" height="100%" src="https://www.youtube.com/embed/9pC2IjvLSKs?autoplay=1&cc_load_policy=1" allowfullscreen></iframe>
  </div>
  <!--Films-->
  <div class="row">
    <div class="container-fluid">
      {movie_tiles}
    </div>
  </div>
</body>
</html>
'''

# A single movie entry html template
movie_tile_content = '''
<div class="col-md-4 col-lg-4 movie-tile text-center" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal" data-target="#trailer">
    <img src="{poster_image_url}" width="220" height="342" alt="poster">
    <h2>{movie_title}</h2>
</div>
'''

def create_movie_tiles_content(movies):
    # The HTML content for this section of the page
    content = ''
    for movie in movies:
        # Extract the youtube ID from the url
        youtube_id_match = re.search(
            r'(?<=v=)[^&#]+', movie.trailer_youtube_url)
        youtube_id_match = youtube_id_match or re.search(
            r'(?<=be/)[^&#]+', movie.trailer_youtube_url)
        trailer_youtube_id = (youtube_id_match.group(0) if youtube_id_match
                              else None)

        # Append the tile for the movie with its content filled in
        content += movie_tile_content.format(
            movie_title=movie.title,
            poster_image_url=movie.poster_image_url,
            trailer_youtube_id=trailer_youtube_id
        )
    return content

def open_movies_page(movies):
    # Create or overwrite the output file
    output_file = open('fresh_tomatoes.html', 'w')

    # Replace the movie tiles placeholder generated content
    rendered_content = main_page_content.format(
        movie_tiles=create_movie_tiles_content(movies))

    # Output the file
    output_file.write(main_page_head + rendered_content)
    output_file.close()

    # open the output file in the browser (in a new tab, if possible)
    url = os.path.abspath(output_file.name)
    webbrowser.open('file://' + url, new=2)
