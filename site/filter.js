const input=document.querySelector('#search');
if(input) input.addEventListener('input',()=>{let count=0;document.querySelectorAll('tbody tr').forEach(row=>{row.hidden=!row.textContent.toLowerCase().includes(input.value.toLowerCase());if(!row.hidden)count++});document.querySelector('#count').textContent=`${count} accounts shown`;});
