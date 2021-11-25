import matplotlib
matplotlib.use('Agg')
import io
import base64
from matplotlib import pyplot
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


class GraphicManager:
    
    def correlate(vectorX, vectorY, figure_url, labelX, labelY):

        fig = Figure()
        axis = fig.add_subplot(1, 1, 1)
        axis.set_xlabel(labelX)
        axis.set_ylabel(labelY)
        axis.scatter(vectorX, vectorY)
        
        # Convert plot to PNG image
        pngImage = io.BytesIO()
        FigureCanvas(fig).print_png(pngImage)
        
        # Encode PNG image to base64 string
        pngImageB64String = "data:image/png;base64,"
        pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
        return pngImageB64String

        # pyplot.scatter(vectorX, vectorY)
        # pyplot.savefig(figure_url)
        # pyplot.xlabel(labelX)
        # pyplot.ylabel(labelY)
