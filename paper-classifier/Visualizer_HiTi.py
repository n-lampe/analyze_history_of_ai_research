import matplotlib.pyplot as plt


# Visualizes HI / TI comparison
class Visualizer_HiTi:

    def visualize_HI_vs_TI(self, data, collection_name, savename):
        ax = plt.figure().gca()
        ax.xaxis.get_major_locator().set_params(integer=True)
        ax.axhline(y=1)
        if collection_name == "AITopics":
            plt.subplots(figsize=(22, 12), dpi=300)
        plt.tick_params(labelleft=False, left=False)
        plt.text(-0.2, 0.71, "Focus on human intelligence")
        plt.xlabel('Year', labelpad=10)
        plt.text(-0.2, -0.75, 'Focus on technical implementation')
        plt.ylim(-0.8, 0.8)
        plt.hlines(0, -1000, 1000)
        data.plot(kind="bar", color="b")
        plt.title("Orientation of papers from the " + collection_name)
        plt.savefig("Diagramme\\MI-vs-TI\\" + savename + ".png", bbox_inches='tight')
        plt.clf()
