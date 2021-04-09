import auv_interface
import numpy as np
import matplotlib.pyplot as plt


class HydroCamel(auv_interface.Auv):
    def __init__(self, _sonar_range, _sonar_angle, _map_size, _initial_position, _velocity, _duration, _mines_map):
        self._sonar_range=_sonar_range
        self._sonar_angle=_sonar_angle
        self._map_size=_map_size
        self._initial_position=_initial_position
        self._velocity=_velocity
        self._velocity_for_heading_angle=[[0,0]]+self._velocity
        self._duration=_duration
        self._mines_map=_mines_map
        self.current_positen=[_initial_position[0],_initial_position[1]]
        self.board=np.zeros(self._map_size) + np.array(_mines_map)
        self.sonar_edges=[]
        self.time_step_counter=0
        self.founded_mines_dict=[]
        self.heading_angle=np.rad2deg(np.arctan2((-self._velocity[0][0]),(self._velocity[0][1]))) #initiel heading angle

        self.get_sonar_fov()
    def get_mines(self):
        #mines=self.founded_mines_dict
        self.sort(self.founded_mines_dict,len(self.founded_mines_dict),0,1)
        count=1
        start=0
        for i in range(len(self.founded_mines_dict)-1):
            if self.founded_mines_dict[i][1]==self.founded_mines_dict[i+1][1]:
                if count == 1:
                    start = i
                count += 1
                if i == len(self.founded_mines_dict)-2:
                    self.sort(self.founded_mines_dict,start+count,start,0)
                elif count > 1:
                    self.sort(self.founded_mines_dict,start+count,start,0)
                    count = 1

        #self.founded_mines_dict=mines
        return self.founded_mines_dict

    def sort(self,l,end,start=0,elemnt=0):
        for i in range(end-start):
            swap=i+np.argmin([i[elemnt] for i in l[start+i:end]])
            (l[i+start], l[swap+start])=(l[swap+start],l[i+start])

    def get_sonar_triangle_ponts(self):
        '''gives the kodkodim of the sonar accorrding to R and angle
         current pisotion is a tuple(x,y) where x is the i elemnt of the matrix and y the j elemnt of the matrix! do not confuse'''
        deg_angle=np.deg2rad(self._sonar_angle)
        b_i = self.current_positen[0]+self._sonar_range*np.sin(deg_angle)
        c_i= self.current_positen[0]-self._sonar_range*np.sin(deg_angle)
        b_j = self.current_positen[1]+self._sonar_range*np.cos(deg_angle)
        c_j= self.current_positen[1]+self._sonar_range*np.cos(deg_angle)
        a_i=self.current_positen[0]
        a_j=self.current_positen[1]
        self._velocity

        #rotain matrix
        # print(b_i,b_j,'not roatetd')
        rotated_b_i = self.rotate_vec(b_i,b_j)[0] 
        rotated_b_j = self.rotate_vec(b_i,b_j)[1] 
        rotated_c_i = self.rotate_vec(c_i,c_j)[0] 
        rotated_c_j = self.rotate_vec(c_i,c_j)[1] 
        # print(rotated_b_i,rotated_b_j,'rotated')

        self.sonar_edges=[a_i,a_j,rotated_b_i,rotated_b_j,rotated_c_i,rotated_c_j]
        # #self.sonar_edges=[a_i,a_j,b_i,b_j,c_i,c_j]
        # print(a_i,a_j,rotated_b_i,rotated_b_j,rotated_c_i,rotated_c_j)
        # print(self.rotate_vec(b_i,b_j)[0],'zero?')

    def rotate_vec(self,i_cord,j_cord): # around zero
        i_cord=i_cord-self.current_positen[0]
        j_cord=j_cord-self.current_positen[1]
        c, s = np.cos(np.deg2rad(self.heading_angle)), np.sin(np.deg2rad(self.heading_angle))
        rotaintion_matrix = np.matrix([[c, s], [-s, c]])
        m = np.dot(rotaintion_matrix, [j_cord, i_cord])
        rotated_j,rotated_i = float(m.T[0]), float(m.T[1])
        rotated_i=rotated_i+self.current_positen[0]
        rotated_j=rotated_j+self.current_positen[1]
        return (rotated_i,rotated_j)

    def check_sonar_triangle(self,a_i,a_j,b_j,b_i,c_j,c_i,p_x,p_y):
        '''input: cordinate of edgdes of traingle (the matrix element)
           output: returs ture if the cordinate is in the sonar'''
        w_1=(a_i*(c_i-a_j)+(p_y-a_j)*(c_j-a_i)-p_x*(c_i-a_j))/((b_i-a_j)*(c_j-a_i)-(b_j-a_i)*(c_i-a_j))
        w_2=(p_y-a_j-w_1*(b_i-a_j))/(c_i-a_j)
        if w_1>=0 and w_2>=0 and (w_1+w_2)<=1:
            return True    
        return False

    def get_sonar_fov(self):
        sonar_dict={}
        self.get_sonar_triangle_ponts()
        for (x,y), value in np.ndenumerate(self.board):
            if self.check_sonar_triangle(self.sonar_edges[0],self.sonar_edges[1],self.sonar_edges[2],self.sonar_edges[3],self.sonar_edges[4],self.sonar_edges[5],x,y) == True :
                #do some thing to element
                sonar_dict.update({(x,y):True})
                if self.board[x,y] == 1 : # its a mokesh
                    self.board[x,y] = 3
                    self.founded_mines_dict.append((x,y))
                else:
                    self.board[x,y]=2
        return sonar_dict

    def remove_privous_sonar_fov(self):
        for (x,y), value in np.ndenumerate(self.board):
            if self.check_sonar_triangle(self.sonar_edges[0],self.sonar_edges[1],self.sonar_edges[2],self.sonar_edges[3],self.sonar_edges[4],self.sonar_edges[5],x,y) == True :
                #do some thing to element
                self.board[x,y]=0        

    def display_map(self):
        plt.show(plt.matshow(self.board))

    def get_heading_inner(self):

        v_y=-self._velocity[0][0]
        v_x=self._velocity[0][1]
        self.heading_angle=np.rad2deg(np.arctan2(v_y,v_x))
        # print(self.heading_angle)
        return self.heading_angle


    def get_heading(self):
        #print(self._velocity_for_heading_angle)
        v_y_n=-self._velocity_for_heading_angle[0][0]
        v_x_n=self._velocity_for_heading_angle[0][1]
        # print(self.heading_angle)
        self._velocity_for_heading_angle=self._velocity
        return np.rad2deg(np.arctan2(v_y_n,v_x_n))

    def set_course(self, _velocity, _duration):

        self._velocity.append(_velocity)
        self._duration.append(_duration)

    def time_step(self):

        if self._duration[0] != 0 :
            #self.get_heading()
            if self.sonar_edges != [] :
                self.remove_privous_sonar_fov()
            self.current_positen[0] = self.current_positen[0]+self._velocity[0][0]
            self.current_positen[1] = self.current_positen[1]+self._velocity[0][1]
            self.get_sonar_fov()
            self._duration[0] = self._duration[0] - 1
            self.get_heading_inner()
        if self._duration[0] == 0 :
            if self._duration != [0]:
                self._velocity=self._velocity[1:]
                self._duration=self._duration[1:]
                self.get_heading_inner()
            else:
                return None
    def start(self):
        #self.get_sonar_fov()
        counter=0
        for i in self._duration:
            counter = counter + i
        for i in range(counter):
            self.time_step()
            #self.display_map()
            self.get_mines()
            self.get_heading_inner()
            #self.display_map()
            self.get_heading()

if __name__ == "__main__":
    '''dsda'''

