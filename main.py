import pandas as pd
import matplotlib.pyplot as plt

# Read the flight simulation data from the text file
data = pd.read_csv("C:\\Game\\jsbsim\\simulation\\hello6.txt", delimiter=',', keep_default_na=False)

# Print the variable names
print(data.columns)

# Access columns using the original names
x = data['X_{ECI} (ft)']
y = data['Y_{ECI} (ft)']
z = data['Altitude ASL (ft)']

# Plot the flight path in 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(x, y, z, linewidth=1.5)  # Corrected from ax.plot3 to ax.plot
ax.set_xlabel('X (ft)')
ax.set_ylabel('Y (ft)')
ax.set_zlabel('Z (ft)')
ax.set_title('Flight Path')
plt.grid(True)

# Add starting and ending point markers
ax.scatter(x.iloc[0], y.iloc[0], z.iloc[0], color='g', label='Start', s=100)  # Added size for visibility
ax.scatter(x.iloc[-1], y.iloc[-1], z.iloc[-1], color='r', label='End', s=100)  # Added size for visibility
ax.legend()

# Extract time and altitude data
time = data['Time']
altitude = data['Altitude ASL (ft)']

# Plot altitude vs. time
plt.figure()
plt.plot(time, altitude, linewidth=1.5)
plt.xlabel('Time (s)')
plt.ylabel('Altitude (ft)')
plt.title('Altitude vs. Time')
plt.grid(True)

# Extract velocity data
velocity = data['V_{Total} (ft/s)']

# Plot velocity vs. time
plt.figure()
plt.plot(time, velocity, linewidth=1.5)
plt.xlabel('Time (s)')
plt.ylabel('Velocity (ft/s)')
plt.grid(True)

# Extract pitch, roll, and yaw data
pitch = data['Theta (deg)']
roll = data['Phi (deg)']
yaw = data['Psi (deg)']

# Plot pitch, roll, and yaw vs. time
plt.figure()

plt.subplot(3, 1, 1)
plt.plot(time, pitch, linewidth=1.5)
plt.xlabel('Time (s)')
plt.ylabel('Pitch (deg)')
plt.title('Pitch')
plt.grid(True)

plt.subplot(3, 1, 2)
plt.plot(time, roll, linewidth=1.5)
plt.xlabel('Time (s)')
plt.ylabel('Roll (deg)')
plt.title('Roll')
plt.grid(True)

plt.subplot(3, 1, 3)
plt.plot(time, yaw, linewidth=1.5)
plt.xlabel('Time (s)')
plt.ylabel('Yaw (deg)')
plt.title('Yaw')
plt.grid(True)

plt.suptitle('Pitch, Roll, and Yaw vs. Time')
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()