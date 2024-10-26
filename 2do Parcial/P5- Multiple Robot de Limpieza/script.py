# %% [markdown]
# ### 1.- Instalar Dependencias

# %%
import agentpy as ap
import matplotlib.pyplot as plt
import numpy as np

# Visualization
import seaborn as sns
import IPython

# %% [markdown]
# ### 2.- Definición de Agentes

# %%
# Complete next_random_position
# Change clenaing room to add more agents
# Don't use next_position
class CleaningRobot(ap.Agent):

    #Constructor
    def setup(self):
      
      # direction atributes
      self.dx = 1
      self.dy = 0



      pass

    #Reglas de desplazamiento
    def setup_rules(self, xlim, ylim):

        # Save displacement limits
        self.xlim = xlim
        self.ylim = ylim


        pass

    #Obtener posicion
    def get_position(self, world):

        # Get agent position in the world
        pos = world.positions[self]
        return pos

    #Obtener estado siguiente
    def get_next_state(self, world):

        # get agent position
        position = self.get_position(world)

        # Verify if the next position is out of the limits
        if position[0] + self.dy < 0 or position[1] + self.dx < 0 or position[0] + self.dy > self.ylim or position[1] + self.dx > self.xlim:
            return [-1]
        else:
            
            # Read next position state
            value = world.agents[(position[0] + self.dy, position[1] + self.dx)].condition

            # convert iteration to state
            values = []
            for i in value:
                values.append(i)

            return values

            

    #Moverse de forma aleatoria
    def next_random_position(self,world):

        # get agent position
        position = self.get_position(world)

        value = self.get_next_state(world)

        # Move agent if the next position is not a hole, obstacle or robot
        if value[0] != -1 and value[0] != 2 and world.agents[(position[0] + self.dy, position[1] + self.dx)].condition == 3:
            world.move_to(self, (position[0] + self.dy, position[1] + self.dx))
        else:
            # Get random direction move in x or y
            random = np.random.choice([1,2])

            if random == 1:
                # Turn randomly to the left or right
                self.dy = np.random.choice([-1,1])
                self.dx = 0
            else:
                # Turn randomly to the top or bottom
                self.dx = np.random.choice([-1,1])
                self.dy = 0
        pass



    #Limpiar area
    def clear_area(self, world):

        # Clean actual position
        position = self.get_position(world)
        world.agents[position].condition = 0

        # Get environment positions
        environment = world.neighbors(self, 1)

        # Clean around positions
        for floor in environment:
            if floor.condition == 1:
                floor.condition = 0 # Change to clean


        pass

# %% [markdown]
# ### 3.- Creación del Ambiente

# %%
class CleaningRoom(ap.Model):

    #Metodo de configuracion
    def setup(self):

        # Create floor agents
        n_floor = int(self.p['dim'] * self.p['dim'])
        self.floor_agents = ap.AgentList(self, n_floor)

        # Create cleaning robot
        self.robot_agents = ap.AgentList(self, self.p['num_robots'], CleaningRobot)

        # Create environment
        self.room = ap.Grid(self, [self.p['dim']]*2, track_empty=True)
        
        # Add agents to the environment
        self.room.add_agents(self.robot_agents, random=True)
        self.room.add_agents(self.floor_agents)

        # Initialize floor status
        # 0: Clean, 1: Dirty, 2: Obstacle
        self.room.agents.condition = 0

        # Set dirty spots
        dirty_index = np.random.randint(len(self.floor_agents), 
                                        size=(int(self.p['den_dirt']*self.p['dim']**2)))
        
        for i in range(len(dirty_index)):
            self.floor_agents[dirty_index[i]].condition = 1


        # Set obstacles
        obstacle_index = np.random.randint(len(self.floor_agents), 
                                        size=(int(self.p['den_obs']*self.p['dim']**2)))
        
        for i in range(len(obstacle_index)):
            self.floor_agents[obstacle_index[i]].condition = 2

        # Assign state to robots
        for i in range(len(self.robot_agents)):
            self.robot_agents[i].condition = 3
            self.room.agents[self.room.positions[self.robot_agents[i]]].condition = 3
                
        # Initialize robots atributtes
        for i in range(len(self.robot_agents)):
            self.robot_agents[i].setup_rules(self.p['dim']-1, self.p['dim']-1)

    #Iteracion
    def step(self):

        # Clean area
        for i in range(len(self.robot_agents)):
            self.robot_agents[i].clear_area(self.room)

        # Move to next position
        for i in range(len(self.robot_agents)):
            self.robot_agents[i].next_random_position(self.room)

        # Get actual positions
        positions = []
        for i in range(len(self.robot_agents)):
            positions.append(self.room.positions[self.robot_agents[i]])

        # Check robots possitions
        for i in range(len(positions)):
            self.room.agents[positions[i]].condition = 3

        pass

    #Finalizar simulacion
    def end(self):

        pass

# %% [markdown]
# ### 4.- Simulación

# %% [markdown]
# Funciones Auxiliares

# %%
#Convertor de RGB a HEX
def rgb2hex(r, g, b):

  var = '#%02x%02x%02x' % (r, g, b)

  return var

# %%
# Create single-run animation with custom colors
def animation_plot(model, ax):
    attr_grid = model.room.attr_grid('condition')
    ap.gridplot(attr_grid, ax=ax, color_dict=color_array, convert=True)

# %% [markdown]
# Parámetros de Simulación

# %%
#Crear paleta de colores
color_array = {0:rgb2hex(255, 255, 255), 1:rgb2hex(200, 200, 200), 2:rgb2hex(0, 0, 0), 3:rgb2hex(0, 255, 0), None:rgb2hex(255, 255, 255)}

# %%
# Inicializar parametros
parameters = {
    'dim': 20, # Scenario dimensions
    'den_obs': 0.1, # % Density of obstacles
    'den_dirt': 0.4, # % Density of dirt
    'num_robots': 5, # Number of robots
}

# %%
#Crear instancia
little_floor = CleaningRoom(parameters)


# %%
#Correr Simulacion
fig, ax = plt.subplots()
animation = ap.animate(little_floor, fig, ax, animation_plot, steps = 200)
IPython.display.HTML(animation.to_jshtml(fps=15))


