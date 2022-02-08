# Hill-Climbing-on-Field-Scanning

Observations were made as a result of the field scanning procedures performed with 1-2-4 drones for 3 different starting points (8.0)-(4.8)-(4.4) given below.

<img width="167" alt="Ekran Resmi 2022-02-08 18 05 29" src="https://user-images.githubusercontent.com/44849765/153014557-afc48ad6-1510-4333-9979-01d69775df36.png">

Two evaluation functions were used in the field scanning algorithm made with hill climbing. These are f1: total area scanned, f2: cost of turning angles. w; If it is considered as the value of goodness; max(f1), min(f2) are requested.

As a result of the trials, it has been observed that the success of the algorithm increases when the population size and the number of generations are kept high and the beginning of the mutation rate is selected low. The w value, which is the combination of the two selected evaluation functions, increased as the number of generations increased and remained constant after a while. This shows that as the number of iterations increased, better paths were found than the best available path, but after a while, if the best path was found, it remained constant. When the best path was found, the mutation rate was reduced, and if no better than the current one was found tk_max times, the mutation rate returned to the baseline. The most successful individual was found at the point where the mutation rate was the lowest.

Aşağıda popülasyon büyüklüğü 200 ve 2000 olan iki farklı deneme için Jenerasyon sayısına göre fitness değeri değişimi ve taranan alanların görüntüsü verilmiştir. Popülasyon büyüklüğünün artmasına bağlı olarak ulaşılabilen w değerinin daha yükseklerde olduğu gözlemlenmiştir.

<img width="540" alt="Ekran Resmi 2022-02-08 18 06 18" src="https://user-images.githubusercontent.com/44849765/153014762-ad0a3994-3334-44a1-ad14-29eda32faedc.png">

<img width="577" alt="Ekran Resmi 2022-02-08 18 02 25" src="https://user-images.githubusercontent.com/44849765/153014216-7d9c11f9-6c1b-4837-b970-6f5731f9b3fc.png">

<img width="524" alt="Ekran Resmi 2022-02-08 18 02 32" src="https://user-images.githubusercontent.com/44849765/153014230-65bc6059-82b9-435d-af90-65ff45b02672.png">

<img width="523" alt="Ekran Resmi 2022-02-08 18 02 39" src="https://user-images.githubusercontent.com/44849765/153014231-a539cea9-5eb7-40d7-a43c-c9e132a60b84.png">

<img width="636" alt="Ekran Resmi 2022-02-08 18 03 17" src="https://user-images.githubusercontent.com/44849765/153014238-954d2e1e-32f2-4481-805f-f94109785e1f.png">

<img width="683" alt="Ekran Resmi 2022-02-08 18 03 30" src="https://user-images.githubusercontent.com/44849765/153014246-0c3a1178-c008-4859-8edf-3a922dda1010.png">
