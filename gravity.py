import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('dark_background')

G = 6.67430e-11  
M = 5.972e24    
dt = 60         

earth_radius = 6371000
radius_initial = 6771000  

velocity_initial = 6500  
z_velocity = 2000  

position = np.array([radius_initial, 0.0, 0.0])
velocity = np.array([0.0, velocity_initial, z_velocity])

lst_x, lst_y, lst_z = [], [], []

plt.ion()
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

ax.set_box_aspect([1, 1, 1])

u = np.linspace(0, 2 * np.pi, 40)
v = np.linspace(0, np.pi, 40)
x_earth = earth_radius * np.outer(np.cos(u), np.sin(v))
y_earth = earth_radius * np.outer(np.sin(u), np.sin(v))
z_earth = earth_radius * np.outer(np.ones(np.size(u)), np.cos(v))

ax.plot_surface(x_earth, y_earth, z_earth, color='violet', alpha=0.8, edgecolor='blue', linewidth=0.3)

ax.set_xlim([-8000000, 8000000])
ax.set_ylim([-8000000, 8000000])
ax.set_zlim([-8000000, 8000000])
ax.set_title('3D Suborbital Crash Simulator')

path_line, = ax.plot([], [], [], 'r-', linewidth=2, label='Trajectory')
satellite_dot, = ax.plot([], [], [], 'ro', label='Satellite')
ax.legend()

def update_frame(frame):
    global position, velocity 
    
    r = np.linalg.norm(position)
    

    if r <= earth_radius:
        velocity = np.array([0.0, 0.0, 0.0])
    else:
        g_acceleration = (G * M) / (r**2)
        direction = -position / r
        acceleration = direction * g_acceleration
        velocity = velocity + acceleration * dt
        

    position = position + velocity * dt  


    lst_x.append(position[0])
    lst_y.append(position[1])
    lst_z.append(position[2])


    path_line.set_data(lst_x, lst_y)
    path_line.set_3d_properties(lst_z)
    

    satellite_dot.set_data([position[0]], [position[1]])
    satellite_dot.set_3d_properties([position[2]])
    

    return path_line, satellite_dot


ani = FuncAnimation(fig, update_frame, frames=1000, interval=20, blit=False)


plt.ioff()
plt.show()