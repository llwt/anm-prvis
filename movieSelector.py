class MovieSelector:
  @property
  def showTransitionError(self) -> bool:
    return self.ownerComponent.par.Showtransitionerror.eval()

  @showTransitionError.setter
  def showTransitionError(self, value: bool):
    self.ownerComponent.par.Showtransitionerror.val = value

  @property
  def activeMovieIndex(self) -> int:
    return self.ownerComponent.par.Activemovie.eval()

  @property
  def inactiveMovieIndex(self) -> int:
    return 1 - self.activeMovieIndex;

  @activeMovieIndex.setter
  def activeMovieIndex(self, val: int):
    self.ownerComponent.par.Activemovie.val = val


  def __init__(self, ownerComponent) -> None:
    self.ownerComponent = ownerComponent
    self.movies = [
      ( ownerComponent.op('moviefilein1'), ownerComponent.op('select_movie1') ),
      ( ownerComponent.op('moviefilein2'), ownerComponent.op('select_movie2') )
    ]
    self.activeMovieIndex = 0
    self.transitioning = False
    self.showTransitionError = False

    [self.unloadMovie(i) for i in range(len(self.movies))]
    print('MovieSelector initialized')

  def unloadMovie(self, index: int):
    print(f'unloading movie container {index}')
    movieIn, select = self.movies[index]
    select.par.top = ''
    movieIn.par.play = 0
    movieIn.par.file = ''
    movieIn.unload()

  def loadMovie(self, index: int, path: str):
    if self.transitioning:
      self.showTransitionError = True
      return

    self.unloadMovie(index)

    print(f'loading movie container {index} with {path}')
    movieIn, _ = self.movies[index]
    movieIn.par.file = path
    movieIn.preload()

  def Play(self, path: str):
    self.loadMovie(self.inactiveMovieIndex, path)

  def OnMovieLoaded(self, movieNumber: float):
    index = int(movieNumber) - 1
    movieIn, select = self.movies[int(index)]

    # Touch likes to randomly toggle the fully_pre_read state when panels/menus
    # are opened for some reason. If we've already loaded the video, we don't 
    # want to set the transitioning state again as onMovieChanged won't be 
    # fired a second time.
    if self.activeMovieIndex == index:
      return

    self.transitioning = True
    print(f'movie {index} loaded')

    movieIn.par.play = 1
    select.par.top = movieIn.path

    self.activeMovieIndex = index

  def OnMovieChanged(self):
    self.unloadMovie(self.inactiveMovieIndex)
    self.transitioning = False
    self.showTransitionError = False