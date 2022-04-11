class MovieSelector:
  @property
  def showTransitionError(self) -> bool:
    return bool(self.ownerComponent.par.Showtransitionerror.eval())

  @showTransitionError.setter
  def showTransitionError(self, value: bool):
    self.ownerComponent.par.Showtransitionerror.val = int(value)

  @property
  def showLoadError(self) -> bool:
    return bool(self.ownerComponent.par.Showloaderror.eval())

  @showLoadError.setter
  def showLoadError(self, value: bool):
    self.ownerComponent.par.Showloaderror.val = int(value)

  @property
  def activeMovieNumber(self) -> int:
    return self.ownerComponent.par.Activemovie.eval()

  @activeMovieNumber.setter
  def activeMovieNumber(self, val: int):
    self.ownerComponent.par.Activemovie.val = val

  @property
  def activeMovie(self) -> op:
    return self.movies[self.activeMovieNumber - 1]

  @property
  def inactiveMovieNumber(self) -> int:
    return 1 if self.activeMovieNumber == 2 else 2

  @property
  def inactiveMovie(self) -> op:
    return self.movies[self.inactiveMovieNumber - 1]

  def __init__(self, ownerComponent) -> None:
    self.ownerComponent = ownerComponent
    self.movies = [
      self.ownerComponent.op('preloadableMovie1'),
      self.ownerComponent.op('preloadableMovie2')
    ]
    for m in self.movies:
      m.par.Unload.pulse()
      m.par.Moviefile.val = ''

    self.activeMovieNumber = 1
    self.transitioning = False
    self.showTransitionError = False
    self.showLoadError = False

    print('MovieSelector initialized')

  def Play(self, path: str):
    if self.transitioning:
      self.showTransitionError = True
      return

    self.showLoadError = False
    self.transitioning = True
    self.inactiveMovie.par.Moviefile.val = path
    self.inactiveMovie.par.Load.pulse()

  def OnMovieLoadError(self, movieNumber: int):
    print(f'error loading movie {movieNumber}')
    self.showLoadError = True
    self.inactiveMovie.par.Unload.pulse()

  def OnMovieLoaded(self, movieNumber: int):
    print(f'movie {movieNumber} loaded')
    self.activeMovieNumber = movieNumber

  def OnMovieChanged(self):
    if self.inactiveMovie.par.State.eval() == 'loaded':
      print(f'active movie is: {self.activeMovieNumber}')
      print(f'unloading {self.inactiveMovieNumber}')
      self.inactiveMovie.par.Unload.pulse()
      self.inactiveMovie.par.Unload.pulse()
    else:
      # reset state to allow movies to be loaded again
      self.OnMovieUnloaded(self.inactiveMovieNumber) 

  def OnMovieUnloaded(self, movieNumber: int):
    self.transitioning = False
    self.showTransitionError = False
