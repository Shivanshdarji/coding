#include<stdio.h>
int soc_kno();

int main ()
{
    char name[10];
    int field,mode;
    printf("\n\nHELLO PLAYER\n\n");
    printf("Please Enter your NAME:");
    scanf("%s",&name);
    // scanf("%c",&name);
    printf("Dear %s\nThe Rules are:\n1)There will be 10 Questions.\n2)Each Player will get 3 Helplines\n",name);
    printf("3)The money will increase accordingly,the final prize will be one CRORE!!!\n");
    printf("4)No Communications are allowed while Playing.");
    printf("press 0 to EXIT THE GAME!!!");
    scanf("%c",&name);
    printf("\n\n\n\nSOO LETS START !!!");
    another:
    scanf("%c",&name);
    printf("\n\n\nPlease select your intrested field\n\n\n");
    scanf("%c",&name);
    printf("The Fields are:\n1)Social Knowledge\n2)Computer Knowledge\n3)Medical/Pharmacuitical\n\nPlease Enter the Number for the field Selction=");
    scanf("%d",&field);
    if(field == 1)
    {
        printf("\nYou Selected Social Knowledge, So Lets Start!!!\n");
        scanf("%c",&name);
        soc_kno();
    printf("GAME OVER!!!\nThank You Playing!!!\n");
    printf("please press 1 for Exit and 2 for Playing in another Mode!!");
    scanf("%d",&mode);
    if(mode==1)
    {
        return 0;
    }
    else if(mode==2)
    goto another;
    
    }
    if(field==2)
    {
        printf("\nYou Selected Computer Knowledge, So Lets Start!!!");
    }
    if(field==3)
    {
        printf("\nYou Selected Pharmaceutical/Medical Knowledge, So Lets Start!!!");
    }
    return 0;
}
int soc_kno()
{
    start:
    char name;
    int ans,exit,mode;
    int ff=1,ex=1,au=1;
    int final;
   
    printf("Before Starting,if You want to use Helplines Type Numbers as Follow \n");
    printf("For 50-50=Type 100\nFor Audience Call=Type 200\nFor Expert Advice=Type 300\nTo see your Left LifeLines PRESS 500\n");
    // printf("Please Finalise your Question,You will get that amount of money of that question,IF YOU LOST!!!");
    // scanf("%d",&final);
    //Question 1
    printf("Question 1:\n");
    scanf("%c",&name);
    printf("The father of Indian missile technology is _________________?\n");
    scanf("%c",&name);
    
    printf("A) Dr Homi Bhabha               B)Dr Chidambaram\n");
    printf("C) APJ Abdul kalam              D)Dr U.R. Rao\n");
    
     ans:
    scanf("%d",&ans);
   
     if(ans==3)
    {
    printf("WOWW!!!\nYOU WON $1000!!!\n");
    } 
    else if(ans==100)
    {
        printf("You Selected 50-50\nA)Dr Homi Bhabha\nC)APJ Abdul Kalam\n");
        ff--;
        
        goto ans;
    } 
    else if(ans==0)
    {
      return 0;
    }
    else if(ans==500)
    {
      printf("Fifty-Fifty=%d\n",ff);
      printf("Expert Advice=%d\n",ex);
      printf("Audience call=%d\n",au);
      printf("Ans:");
      goto ans;
    }
    else if(ans==200)
    {printf("You Selected Audience Call\nOption A=12%%\nOption B=9%%\nOption C=69%%\nOption D=10%%\nNow PLease Ans:");
    au--;
    goto ans;
    }
    else if(ans==300)
   { printf("You Selected Expert Advice\nYour Expert here is MR SHIVANSH DARJI.");
   ex--;
   goto ans;
   }
     else //if(ans=='A'||'B'||'D'||'a'||'b'||'d')
    { 
     printf("SORRY! Wrong ANS!!!\n");
     printf("For Playing again please enter '1' AND for Exit please Enter '2':");
     scanf("%d",&exit);
     if(exit==2)
      return 0;
    else if(exit==1)
      goto start;
   }
   /*Question 2
   
   
   */
  scanf("%c",&name);
   printf("Question 2:\n");
    scanf("%c",&name);
    printf("Which of the following Himalayan regions is called Shivalik's?\n");
    scanf("%c",&name);
    
    printf("A) Upper Himalayas              B)Lower Himalayas\n");
    printf("C) Outer Himalayas              D)Inner Himalayas\n");
    ans1:
    scanf("%d",&ans);
     if(ans==3)
    {
    printf("WOWW!!!\nYOU WON $5000!!!\n");
    }
    else if(ans==0)
    {
      return 0;
    } 
     else if(ans==500)
    {
      printf("Fifty-Fifty=%d\n",ff);
      printf("Expert Advice=%d\n",ex);
      printf("Audience call=%d\n",au);
      printf("Ans:");
      goto ans1;
    }
    else if(ans==100)
    {
      if(ff==0)
      printf("You Used this option");
      else
        {printf("You Selected 50-50\n                                B)Lower Himalayas\nC)Outer Himalayas\nAns:");
        ff--;}
        goto ans1;
    } 
    else if(ans==200)
    {if(au==0)
      printf("You Used this option");
      else{
      printf("You Selected Audience Call\nOption A=6%%\nOption B=38%%\nOption C=39%%\nOption D=17%%\nNow PLease Ans:");
      au--;}
    goto ans1;
    }
    else if(ans==300)
   {if(ex==0)
   printf("You used this before");
   else{ printf("You Selected Expert Advice\nYour Expert here is MR SHIVANSH DARJI.\n Ans:");
   ex--;}
   goto ans1;
   }
     else //if(ans=='A'||'B'||'D'||'a'||'b'||'d')
    { 
     printf("SORRY! Wrong ANS!!!\n");
     printf("For Playing again please enter '1' AND for Exit please Enter '2':");
     scanf("%d",&exit);
     if(exit==2)
      return 0;
    else if(exit==1)
      goto start;
    }
    /*Question 3
   
   
   */
  scanf("%c",&name);
   printf("Question 3:\n");
    scanf("%c",&name);
    printf("Which of the given cities is located on the bank of river Ganga?\n");
    scanf("%c",&name);
    
    printf("A) Patna                        B)Bihar\n");
    printf("C) Bhopal                       D)Mathura\n");
    ans2:
    scanf("%d",&ans);
     if(ans==1)
    {
    printf("WOWW!!!\nYOU WON $10000!!!\n");
    } 
    else if(ans==0)
    {
      return 0;
    }
     else if(ans==500)
    {
      printf("Fifty-Fifty=%d\n",ff);
      printf("Expert Advice=%d\n",ex);
      printf("Audience call=%d\n",au);
      printf("Ans:");
      goto ans2;
    }
    else if(ans==100)
    {
      if(ff==0)
      printf("You Used this option");
      else
       { printf("You Selected 50-50\nA)Patna                         B)Bihar\nAns:");
       ff--;}
        goto ans2;
    } 
    else if(ans==200)
    {if(au==0)
      printf("You Used this option");
      else
     { printf("You Selected Audience Call\nOption A=39%%\nOption B=38%%\nOption C=8%%\nOption D=15%%\nNow PLease Ans:");
     au--;}
    goto ans2;
    }
    else if(ans==300)
   { if(ex==0)
   printf("You used this before");
   else{printf("You Selected Expert Advice\nYour Expert here is MR SHIVANSH DARJI.\n Ans:");
   ex--;}
   goto ans2;
   }
     else //if(ans=='A'||'B'||'D'||'a'||'b'||'d')
    { 
     printf("SORRY! Wrong ANS!!!\n");
     printf("For Playing again please enter '1' AND for Exit please Enter '2':");
     scanf("%d",&exit);
     if(exit==2)
      return 0;
    else if(exit==1)
      goto start;
    }
     /*Question 4
   
   
   */
  scanf("%c",&name);
   printf("Question 4:\n");
    scanf("%c",&name);
    printf(" Who was the first President of independent India?\n");
    scanf("%c",&name);
    
    printf("A)S. Radhakrishnan                        B)Rajendra Prasad\n");
    printf("C)Indira Gndhi                            D)Javaharlal Nahru\n");
    ans3:
    scanf("%d",&ans);
     if(ans==2)
    {
    printf("WOWW!!!\nYOU WON $50000!!!\n");
    } 
    else if(ans==0)
    {
      return 0;
    }
     else if(ans==500)
    {
      printf("Fifty-Fifty=%d\n",ff);
      printf("Expert Advice=%d\n",ex);
      printf("Audience call=%d\n",au);
      printf("Ans:");
      goto ans3;
    }
    else if(ans==100)
    {
      if(ff==0)
      printf("You Used this option");
      else
       { printf("You Selected 50-50\nA)S. Radhakrishnan             B)Rajendra Prasad\nAns:");
       ff--;}
        goto ans3;
    } 
    else if(ans==200)
    {if(au==0)
      printf("You Used this option");
      else{printf("You Selected Audience Call\nOption A=11%%\nOption B=6%%\nOption C=41%%\nOption D=42%%\nNow PLease Ans:");
      au--;}
    goto ans3;
    }
    else if(ans==300)
   { if(ex==0)
   printf("You used this before");
   else{printf("You Selected Expert Advice\nYour Expert here is MR SHIVANSH DARJI.\n Ans:");
   ex--;}
   goto ans3;
   }
     else //if(ans=='A'||'B'||'D'||'a'||'b'||'d')
    { 
     printf("SORRY! Wrong ANS!!!\n");
     printf("For Playing again please enter '1' AND for Exit please Enter '2':");
     scanf("%d",&exit);
     if(exit==2)
      return 0;
    else if(exit==1)
      goto start;
    }
     /*Question 5
   
   
   */
  scanf("%c",&name);
   printf("Question 5:\n");
    scanf("%c",&name);
    printf("Who was the first Indian woman to win a medal in the Olympics?\n");
    scanf("%c",&name);
    
    printf("A)P.T. Usha                       B)Kunjarani Devi\n");
    printf("C)Bachendri Pal                   D)D.Karnam Maleshwari\n");
    ans4:
    scanf("%d",&ans);
     if(ans==4)
    {
    printf("WOWW!!!\nYOU WON $100000!!!\n");
    } 
     else if(ans==500)
    {
      printf("Fifty-Fifty=%d\n",ff);
      printf("Expert Advice=%d\n",ex);
      printf("Audience call=%d\n",au);
      printf("Ans:");
      goto ans4;
    }
    else if(ans==0)
    {
      return 0;
    }
    else if(ans==100)
    {
      if(ff==0)
      printf("You Used this option");
      else
       { printf("You Selected 50-50\nA)P.T. Usha\n                                  D)D.Karnam Maleshwari\nAns:");
         ff--;}
         goto ans4;
    } 
    else if(ans==200)
    {if(au==0)
      printf("You Used this option");
      else{printf("You Selected Audience Call\nOption A=11%%\nOption B=6%%\nOption C=41%%\nOption D=42%%\nNow PLease Ans:");
      au--;}
    goto ans4;
    }
    else if(ans==300)
   {if(ex==0)
    printf("You Used this befor");
    else{ printf("You Selected Expert Advice\nYour Expert here is MR SHIVANSH DARJI.\n Ans:");
    ex--;}
   goto ans4;
   }
     else //if(ans=='A'||'B'||'D'||'a'||'b'||'d')
    { 
     printf("SORRY! Wrong ANS!!!\n");
     printf("For Playing again please enter '1' AND for Exit please Enter '2':");
     scanf("%d",&exit);
     if(exit==2)
      return 0;
    else if(exit==1)
      goto start;
    }
     /*Question 6
   
   
   */
  scanf("%c",&name);
   printf("Question 6:\n");
    scanf("%c",&name);
    printf("Who was the first Indian to climb Mount Everest?\n");
    scanf("%c",&name);
    
    printf("A)Anshu Jamsenpa                 B)Avatar Singh Cheema\n");
    printf("C)Santosh Yadav                  D)Jyoti Ratre\n");
    ans5:
    scanf("%d",&ans);
     if(ans==2)
    {
    printf("WOWW!!!\nYOU WON $1000000!!!\n");
    }
    else if(ans==0)
    {
      return 0;
    } 
    else if(ans==100)
    {
      if(ff==0)
      printf("You Used this option");
      else
       { printf("You Selected 50-50\nA)                                 B)Avatar Singh Cheema\nC)Santosh Yadav\nAns:");
       ff--;}
        goto ans5;
    } 
     else if(ans==500)
    {
      printf("Fifty-Fifty=%d\n",ff);
      printf("Expert Advice=%d\n",ex);
      printf("Audience call=%d\n",au);
      printf("Ans:");
      goto ans5;
    }
    else if(ans==200)
    {if(au==0)
      printf("You Used this option");
      else{printf("You Selected Audience Call\nOption A=1%%\nOption B=36%%\nOption C=41%%\nOption D=22%%\nNow PLease Ans:");
      au--;}
    goto ans5;
    }
    else if(ans==300)
   {if(ex==0)
    printf("You Used this befor");
    else{ printf("You Selected Expert Advice\nYour Expert here is MR SHIVANSH DARJI.\n Ans:");
    ex--;}
   goto ans5;
   }
     else //if(ans=='A'||'B'||'D'||'a'||'b'||'d')
    { 
     printf("SORRY! Wrong ANS!!!\n");
     printf("For Playing again please enter '1' AND for Exit please Enter '2':");
     scanf("%d",&exit);
     if(exit==2)
      return 0;
    else if(exit==1)
      goto start;
    }
 /*Question 7
   
   
   */
  scanf("%c",&name);
   printf("Question 7:\n");
    scanf("%c",&name);
    printf("Here the Song Played carefully and tell the name of the movie of the song?\n");
    scanf("%c",&name);
    
    printf("A)Anand                     B)Sanjog\n");
    printf("C)Ek nazar                  D)Rastee ka pathar\n");
    ans6:
    scanf("%d",&ans);
     if(ans==2)
    {
    printf("WOWW!!!\nYOU WON $2500000!!!\n");
    } 
    else if(ans==0)
    {
      return 0;
    }
    else if(ans==100)
    {
      if(ff==0)
      printf("You Used this option");
      else
      {
        printf("You Selected 50-50\nA)Anand                          B)Sanjog\nAns:");
        ff--;}
        goto ans6;
    }
     else if(ans==500)
    {
      printf("Fifty-Fifty=%d\n",ff);
      printf("Expert Advice=%d\n",ex);
      printf("Audience call=%d\n",au);
      printf("Ans:");
      goto ans6;
    } 
    else if(ans==200)
    {if(au==0)
      printf("You Used this option");
      else{printf("You Selected Audience Call\nOption A=1%%\nOption B=46%%\nOption C=21%%\nOption D=22%%\nNow PLease Ans:");
      au--;}
    goto ans6;
    }
    else if(ans==300)
   {if(ex==0)
    printf("You Used this befor");
    else{ printf("You Selected Expert Advice\nYour Expert here is MR SHIVANSH DARJI.\n Ans:");
    ex--;}
   goto ans6;
   }
     else //if(ans=='A'||'B'||'D'||'a'||'b'||'d')
    { 
     printf("SORRY! Wrong ANS!!!\n");
     printf("For Playing again please enter '1' AND for Exit please Enter '2':");
     scanf("%d",&exit);
     if(exit==2)
      return 0;
    else if(exit==1)
      goto start;
    }

/*Question 8
   
   
   */
  scanf("%c",&name);
   printf("Question 8:\n");
    scanf("%c",&name);
    printf("The worlds first national 5G mobile network was launched by which country?\n");
    scanf("%c",&name);
    
    printf("A)Japan                    B)Asia\n");
    printf("C)South Korea              D)America\n");
    ans7:
    scanf("%d",&ans);
     if(ans==3)
    {
    printf("WOWW!!!\nYOU WON $5000000!!!\n");
    } 
    else if(ans==0)
    {
      return 0;
    }
    else if(ans==100)
    {
      if(ff==0)
      printf("You Used this option");
      else
      {  printf("You Selected 50-50\nA)                         B)\nC)South Korea              D)America\nAns:");
      ff--;}
        
        goto ans7;
    }
     else if(ans==500)
    {
      printf("Fifty-Fifty=%d\n",ff);
      printf("Expert Advice=%d\n",ex);
      printf("Audience call=%d\n",au);
      printf("Ans:");
      goto ans7;
    } 
    else if(ans==200)
    {if(au==0)
      printf("You Used this option");
      else{printf("You Selected Audience Call\nOption A=31%%\nOption B=16%%\nOption C=21%%\nOption D=22%%\nNow PLease Ans:");
      au--;}
    goto ans7;
    }
    else if(ans==300)
   {if(ex==0)
    printf("You Used this befor");
    else{ printf("You Selected Expert Advice\nYour Expert here is MR SHIVANSH DARJI.\n Ans:");
    ex--;}
   goto ans7;
   }
     else //if(ans=='A'||'B'||'D'||'a'||'b'||'d')
    { 
     printf("SORRY! Wrong ANS!!!\n");
     printf("For Playing again please enter '1' AND for Exit please Enter '2':");
     scanf("%d",&exit);
     if(exit==2)
      return 0;
    else if(exit==1)
      goto start;
    }
    /*Question 9
   
   
   */
  scanf("%c",&name);
   printf("Question 9:\n");
    scanf("%c",&name);
    printf("Which of the Caves are Located in Gujarat?\n");
    scanf("%c",&name);
    
    printf("A)Ajanta Ellora                    B)Elephanta\n");
    printf("C)Kapra Khodia                    D)Mujkund Caves\n");
    ans8:
    scanf("%d",&ans);
     if(ans==3)
    {
    printf("WOWW!!!\nYOU WON $7500000!!!\n");
    } 
    else if(ans==0)
    {
      return 0;
    }
    else if(ans==100)
    {
      if(ff==0)
      printf("You Used this option");
      else
       { printf("You Selected 50-50\nA)                         B)\nC)Kapra Khodia              D)Mujkund\nAns:");
       ff--;}
        
        goto ans8;
    }
     else if(ans==500)
    {
      printf("Fifty-Fifty=%d\n",ff);
      printf("Expert Advice=%d\n",ex);
      printf("Audience call=%d\n",au);
      printf("Ans:");
      goto ans8;
    } 
    else if(ans==200)
    {if(au==0)
      printf("You Used this option");
      else{printf("You Selected Audience Call\nOption A=11%%\nOption B=16%%\nOption C=31%%\nOption D=22%%\nNow PLease Ans:");
      au--;}
    goto ans8;
    }
    else if(ans==300)
   { if(ex==0)
    printf("You Used this befor");
    else{printf("You Selected Expert Advice\nYour Expert here is MR SHIVANSH DARJI.\n Ans:");
    ex--;}
   goto ans8;
   }
     else //if(ans=='A'||'B'||'D'||'a'||'b'||'d')
    { 
     printf("SORRY! Wrong ANS!!!\n");
     printf("For Playing again please enter '1' AND for Exit please Enter '2':");
     scanf("%d",&exit);
     if(exit==2)
      return 0;
    else if(exit==1)
      goto start;
    }
     /*Question 10
   
   
   */
  scanf("%c",&name);
   printf("Question 10:\n");
    scanf("%c",&name);
    printf("Which colonial power ended its involvement in India by selling the rights of the Nicobar Islands to the British on October 18, 1868?\n");
    scanf("%c",&name);
    
    printf("A)Belgium                    B)Italy \n");
    printf("C)Denmark                    D)France\n");
    ans9:
    scanf("%d",&ans);
     if(ans==3)
    {
    printf("WOWW!!!\nYOU WON $10000000!!!\n");
    }
    else if(ans==0)
    {
      return 0;
    }
     else if(ans==500)
    {
      printf("Fifty-Fifty=%d\n",ff);
      printf("Expert Advice=%d\n",ex);
      printf("Audience call=%d\n",au);
      printf("Ans:");
      goto ans;
    }
    else if(ans==100)
    {
      if(ff==0)
      printf("You Used this option");
      else
       { printf("You Selected 50-50\nA)                         B)Itley\nC)Denmark                  D)\nAns:");
       ff--;}
        
        goto ans9;
    } 
    else if(ans==200)
    {if(au==0)
      printf("You Used this option");
      else{printf("You Selected Audience Call\nOption A=11%%\nOption B=16%%\nOption C=31%%\nOption D=22%%\nNow PLease Ans:");
      au--;}
    goto ans9;
    }
    else if(ans==300)
   {if(ex==0)
    printf("You Used this befor");
    else{printf("You Selected Expert Advice\nYour Expert here is MR SHIVANSH DARJI.\n Ans:");}
   goto ans9;
   }
     else //if(ans=='A'||'B'||'D'||'a'||'b'||'d')
    { 
     printf("SORRY! Wrong ANS!!!\n");
     printf("For Playing again please enter '1' AND for Exit please Enter '2':");
     scanf("%d",&exit);
     if(exit==2)
      return 0;
    else if(exit==1)
      goto start;
    }
}